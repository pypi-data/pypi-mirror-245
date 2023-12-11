"""A Chess Board."""

from collections import Counter
from collections.abc import Callable, Iterator
from contextlib import contextmanager, suppress
from csv import DictReader
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from platform import system
from random import shuffle
from re import findall, search, sub
from typing import Literal

with suppress(ImportError):
    from rich.console import Console

try:
    from consolechess import utils
except ImportError:
    import utils  # type: ignore

PieceType = Literal["king", "queen", "rook", "bishop", "knight", "pawn"]
Color = Literal["white", "black"]
Side = Literal["kingside", "queenside"]
StatusDescription = Literal[
    "checkmate",
    "stalemate",
    "opponent_resignation",
    "agreement",
    "threefold_repetition",
    "fivefold_repetition",
    "the_50_move_rule",
    "the_75_move_rule",
    "insufficient_material",
]
SquareGenerator = Callable[[str], Iterator[str]]
StepFunction = Callable[[str, int], str]


@dataclass(unsafe_hash=True, frozen=True)
class Piece:
    """A piece on a chess board."""

    piece_type: PieceType
    color: Color


@dataclass(frozen=True)
class GameStatus:
    """Status of the chess game (win/loss/neither)."""

    game_over: bool
    winner: Color | None = None
    description: StatusDescription | None = None


@dataclass(frozen=True)
class Opening:
    """An ECO game opening."""

    eco: str
    name: str
    moves: str


COLORS: tuple[Color, Color] = ("white", "black")
SIDES: tuple[Side, Side] = ("queenside", "kingside")
FILES = list("abcdefgh")
SQUARES = [f"{file}{rank}" for rank in range(1, 9) for file in FILES]
PIECE_SYMBOLS: dict[PieceType, str] = {
    "king": "♚",
    "queen": "♛",
    "rook": "♜",
    "bishop": "♝",
    "knight": "♞",
    "pawn": "♟︎" if "Windows" not in system() else ":chess_pawn:",
}
BLACK_SQUARES = [f"{file}{rank}" for file in "aceg" for rank in (1, 3, 5, 7)] + [
    f"{file}{rank}" for file in "bdfh" for rank in (2, 4, 6, 8)
]
WHITE_SQUARES = [sq for sq in SQUARES if sq not in BLACK_SQUARES]
PLAINTEXT_ABBRS: dict[str, str] = {
    "knight": "N",
    "rook": "R",
    "bishop": "B",
    "pawn": "P",
    "queen": "Q",
    "king": "K",
}
ALGEBRAIC_PIECE_ABBRS: dict[str, PieceType] = {
    "K": "king",
    "Q": "queen",
    "R": "rook",
    "B": "bishop",
    "N": "knight",
    "": "pawn",
}
FEN_REPRESENTATIONS: dict[str, Piece] = {
    "N": Piece("knight", "white"),
    "K": Piece("king", "white"),
    "R": Piece("rook", "white"),
    "B": Piece("bishop", "white"),
    "Q": Piece("queen", "white"),
    "P": Piece("pawn", "white"),
    "n": Piece("knight", "black"),
    "k": Piece("king", "black"),
    "r": Piece("rook", "black"),
    "b": Piece("bishop", "black"),
    "q": Piece("queen", "black"),
    "p": Piece("pawn", "black"),
}
PIECES: list[Piece] = [
    *([Piece("rook", "white")] * 2),
    *([Piece("knight", "white")] * 2),
    *([Piece("bishop", "white")] * 2),
    Piece("queen", "white"),
    Piece("king", "white"),
    *([Piece("pawn", "white")] * 8),
    *([Piece("rook", "black")] * 2),
    *([Piece("knight", "black")] * 2),
    *([Piece("bishop", "black")] * 2),
    Piece("queen", "black"),
    Piece("king", "black"),
    *([Piece("pawn", "black")] * 8),
]
KNIGHT_MOVES = [
    ((up_down, i_1), (left_right, i_2))
    for up_down in ("up", "down")
    for left_right in ("left", "right")
    for i_1, i_2 in ((1, 2), (2, 1))
]
CASTLING_FINAL_SQUARES: dict[tuple[Color, Side], tuple[str, str]] = {
    ("white", "kingside"): ("g1", "f1"),  # color, side: rook, king
    ("white", "queenside"): ("c1", "d1"),
    ("black", "kingside"): ("g8", "f8"),
    ("black", "queenside"): ("c8", "d8"),
}
DIRECTION_GENERATORS: dict[tuple[str, str], SquareGenerator] = {
    ("up", "right"): utils.iter_top_right_diagonal,
    ("up", "inline"): utils.iter_to_top,
    ("up", "left"): utils.iter_top_left_diagonal,
    ("inline", "right"): utils.iter_to_right,
    ("inline", "left"): utils.iter_to_left,
    ("down", "right"): utils.iter_bottom_right_diagonal,
    ("down", "inline"): utils.iter_to_bottom,
    ("down", "left"): utils.iter_bottom_left_diagonal,
}
STEP_FUNCTIONS_BY_DIRECTION: dict[str, StepFunction] = {
    "up": utils.step_up,
    "right": utils.step_right,
    "left": utils.step_left,
    "down": utils.step_down,
    "up_right": utils.step_diagonal_up_right,
    "up_left": utils.step_diagonal_up_left,
    "down_right": utils.step_diagonal_down_right,
    "down_left": utils.step_diagonal_down_left,
}
ROOK_GENERATORS: list[SquareGenerator] = [
    utils.iter_to_top,
    utils.iter_to_bottom,
    utils.iter_to_right,
    utils.iter_to_left,
]
BISHOP_GENERATORS: list[SquareGenerator] = [
    utils.iter_bottom_left_diagonal,
    utils.iter_bottom_right_diagonal,
    utils.iter_top_left_diagonal,
    utils.iter_top_right_diagonal,
]
QUEEN_GENERATORS: list[SquareGenerator] = ROOK_GENERATORS + BISHOP_GENERATORS


class InvalidMoveError(Exception):
    """Raised when move is not allowed."""


class InvalidNotationError(Exception):
    """Raised when chess notation is not valid."""


class OtherPlayersTurnError(Exception):
    """Raised if player moves a white piece on black's turn or vice-versa."""


class ChessBoard:
    """A chess board."""

    def __init__(
        self: "ChessBoard",
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a chess board object."""
        self.grid: dict[str, Piece | None] = {sq: None for sq in SQUARES}
        if not empty and fen is None:
            self.set_staunton_pattern()
        self.white_king_has_moved: bool = False
        self.white_king_init_sq: str | None = None
        self.black_king_has_moved: bool = False
        self.black_king_init_sq: str | None = None
        self.black_queenside_rook_has_moved: bool = False
        self.black_queenside_rook_init_sq: str | None = None
        self.black_kingside_rook_has_moved: bool = False
        self.black_kingside_rook_init_sq: str | None = None
        self.white_queenside_rook_has_moved: bool = False
        self.white_queenside_rook_init_sq: str | None = None
        self.white_kingside_rook_has_moved: bool = False
        self.white_kingside_rook_init_sq: str | None = None
        self.double_forward_last_move: str | None = None
        self.turn: Color = "white"
        self._game_over: bool = False
        self._winner: Color | None = None
        self._status_description: StatusDescription | None = None
        self._variant: str | None = None
        self.halfmove_clock = 0
        self.moves: list[str] = []
        self.moves_before_fen_import = 0
        self.hashes: list[int] = []
        self.initial_fen: str | None = None
        self._event: str | None = None
        self._site: str | None = None
        self._date: str | None = None
        self._round: str | None = None
        self._white: str | None = None
        self._black: str | None = None
        self._fields: list[tuple[str, str]] = []
        self._move_annotations: dict[str, str] = {}
        if fen is not None:
            self.import_fen(fen)
        if pgn is not None:
            self.import_pgn(pgn, import_fields=import_fields)
            return None
        with suppress(StopIteration):
            self.set_initial_positions()

    def __getitem__(self: "ChessBoard", square: str) -> Piece | None:
        """Get a square's current piece, or None if empty."""
        return self.grid[square]

    def __setitem__(self: "ChessBoard", square: str, value: Piece | None) -> None:
        """Set a square to a piece or None if setting to empty."""
        self.grid[square] = value

    def __delitem__(self: "ChessBoard", square: str) -> None:
        """Delete a piece with `del` keyword."""
        self.grid[square] = None

    def __iter__(self: "ChessBoard") -> Iterator[str]:
        """Iterate through board."""
        return iter(self.grid)

    def __hash__(self: "ChessBoard") -> int:
        """Hash board grid string representation."""
        return hash(
            (
                self.black_king_has_moved,
                self.white_king_has_moved,
                self.black_kingside_rook_has_moved,
                self.black_queenside_rook_has_moved,
                self.white_kingside_rook_has_moved,
                self.white_queenside_rook_has_moved,
                self.turn,
                self.double_forward_last_move,
                *self.grid.items(),
            )
        )

    def __repr__(self: "ChessBoard") -> str:
        """Represent ChessBoard as string."""
        return f"ChessBoard('{self.fen}')"

    def get_opening(self: "ChessBoard") -> Opening | None:
        """Get the ECO opening."""
        path = (
            Path(f"{Path(__file__).parent}/openings.csv")
            if "__file__" in globals()
            else Path("openings.csv")
        )
        moves = self.export_moves()
        with path.open() as file:
            candidates = [
                opening for opening in DictReader(file) if opening["moves"] in moves
            ]
        longest_len = 0
        if len(candidates) == 0:
            return None
        for candidate in candidates:
            length = len(candidate["moves"])
            if length > longest_len:
                longest = candidate
                longest_len = length
        return Opening(eco=longest["ECO"], name=longest["name"], moves=longest["moves"])

    def alternate_turn(
        self: "ChessBoard",
        *,
        reset_halfmove_clock: bool = False,
        skip_hash: bool = False,
    ) -> None:
        """
        Alternate turn from white to black or black to white.
        If reset_capture is True, moves_since_capture will be set to 0.
        """
        self.turn = "black" if self.turn == "white" else "white"
        if not skip_hash:
            self.hashes.append(hash(self))
        if reset_halfmove_clock:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

    def set_staunton_pattern(self: "ChessBoard") -> None:
        """Add Staunton pattern (initial piece squares)."""
        self.empty_board()
        empty_squares = [f"{file}{rank}" for file in FILES for rank in range(3, 7)]
        for square in empty_squares:
            self[square] = None
        for square in [f"{file}2" for file in FILES]:
            self[square] = Piece("pawn", "white")
        for square in [f"{file}7" for file in FILES]:
            self[square] = Piece("pawn", "black")
        piece_rows: list[tuple[str, Color]] = [("8", "black"), ("1", "white")]
        for rank, color in piece_rows:
            self[f"a{rank}"] = Piece("rook", color)
            self[f"b{rank}"] = Piece("knight", color)
            self[f"c{rank}"] = Piece("bishop", color)
            self[f"d{rank}"] = Piece("queen", color)
            self[f"e{rank}"] = Piece("king", color)
            self[f"f{rank}"] = Piece("bishop", color)
            self[f"g{rank}"] = Piece("knight", color)
            self[f"h{rank}"] = Piece("rook", color)
        self.set_initial_positions()

    @contextmanager
    def test_position(
        self: "ChessBoard", changes: dict[str, Piece | None]
    ) -> Iterator[None]:
        """
        Make temporary changes to the board to test properties of a position.
        Do not raise exceptions within a `test_position` context manager.
        """
        original_contents = {sq: self[sq] for sq in changes}
        for sq in changes:
            self[sq] = changes[sq]
        yield
        for sq in original_contents:
            self[sq] = original_contents[sq]

    def set_random(self: "ChessBoard") -> None:
        """Set board for Fischer random chess / Chess960."""
        self.empty_board()
        # Set pawns.
        ranks_and_colors: list[tuple[int, Color]] = [(2, "white"), (7, "black")]
        for rank, color in ranks_and_colors:
            for file in FILES:
                self[f"{file}{rank}"] = Piece("pawn", color)
        # Set major pieces.
        major_pieces = [
            "knight",
            "knight",
            "bishop_1",
            "bishop_2",
            "rook_1",
            "rook_2",
            "queen",
            "king",
        ]
        while True:
            shuffle(major_pieces)
            # Check if bishops are on opposite-color squares.
            bishop_1 = f"a{major_pieces.index('bishop_1')}"
            bishop_2 = f"a{major_pieces.index('bishop_2')}"
            if (bishop_1 in BLACK_SQUARES and bishop_2 in BLACK_SQUARES) or (
                bishop_1 in WHITE_SQUARES and bishop_2 in WHITE_SQUARES
            ):
                continue
            # Check if king is in between rooks.
            rook_1_rank = major_pieces.index("rook_1")
            rook_2_rank = major_pieces.index("rook_2")
            a_side_rook = rook_1_rank if rook_1_rank < rook_2_rank else rook_2_rank
            h_side_rook = rook_1_rank if a_side_rook == rook_2_rank else rook_1_rank
            king_rank = major_pieces.index("king")
            if king_rank > h_side_rook or king_rank < a_side_rook:
                continue
            break
        # Populate board.
        major_rank_and_colors: list[tuple[int, Color]] = [(1, "white"), (8, "black")]
        for rank, color in major_rank_and_colors:
            for i, piece in enumerate(major_pieces):
                pt: PieceType = piece.removesuffix("_1").removesuffix("_2")  # type: ignore
                self[f"{FILES[i]}{rank}"] = Piece(pt, color)
        self.set_initial_positions()
        self.initial_fen = self.fen
        self._variant = "Chess960"

    def set_initial_positions(self: "ChessBoard") -> None:
        """Set initial positions of pieces used for castling."""
        white_rooks = [sq for sq in SQUARES if self[sq] == Piece("rook", "white")]
        black_rooks = [sq for sq in SQUARES if self[sq] == Piece("rook", "black")]
        if len(white_rooks) == 2:
            self.white_queenside_rook_init_sq = (
                white_rooks[0]
                if FILES.index(white_rooks[0][0]) < FILES.index(white_rooks[1][0])
                else white_rooks[1]
            )
            self.white_kingside_rook_init_sq = (
                white_rooks[0]
                if self.white_queenside_rook_init_sq != white_rooks[0]
                else white_rooks[1]
            )
        elif len(white_rooks) == 1:
            self.white_queenside_rook_init_sq = white_rooks[0]
            self.white_kingside_rook_init_sq = white_rooks[0]
        if len(black_rooks) == 2:
            self.black_queenside_rook_init_sq = (
                black_rooks[0]
                if FILES.index(black_rooks[0][0]) < FILES.index(black_rooks[1][0])
                else black_rooks[1]
            )
            self.black_kingside_rook_init_sq = (
                black_rooks[0]
                if self.black_queenside_rook_init_sq != black_rooks[0]
                else black_rooks[1]
            )
        elif len(black_rooks) == 1:
            self.black_queenside_rook_init_sq = black_rooks[0]
            self.black_kingside_rook_init_sq = black_rooks[0]
        self.white_king_init_sq = next(
            sq for sq in SQUARES if self[sq] == Piece("king", "white")
        )
        self.black_king_init_sq = next(
            sq for sq in SQUARES if self[sq] == Piece("king", "black")
        )

    def import_pgn(self: "ChessBoard", pgn: str, *, import_fields: bool = True) -> None:
        """Import a game by PGN string."""
        if "[FEN " in pgn:
            with suppress(AttributeError):
                fen = search(r"\[FEN \"(.+?)\"\]", pgn).group(1)  # type: ignore
                self.import_fen(fen)
        self.set_initial_positions()
        self.submit_moves(pgn)
        if import_fields:
            if event := search(r"\[Event \"(.+?)\"\]", pgn):
                self._event = event.group(1)
            if site := search(r"\[Site \"(.+?)\"\]", pgn):
                self._site = site.group(1)
            if date := search(r"\[Date \"(.+?)\"\]", pgn):
                self._date = date.group(1)
            if round := search(r"\[Round \"(.+?)\"\]", pgn):
                self._round = round.group(1)
            if white := search(r"\[White \"(.+?)\"\]", pgn):
                self._white = white.group(1)
            if black := search(r"\[Black \"(.+?)\"\]", pgn):
                self._black = black.group(1)
            self._fields.extend(
                (
                    (name, value)
                    for name, value in findall(r"\[([^\s]+) \"(.+?)\"\]", pgn)
                    if name
                    not in (
                        "Event",
                        "Site",
                        "Date",
                        "Round",
                        "White",
                        "Black",
                        "Result",
                        "CurrentPosition",
                        "FEN",
                    )
                )
            )
            self._move_annotations = dict(
                findall(r"(?P<Move>\d+\.+)[^\.\{]+?\{(?P<Comment>.+?)\}", pgn)
            )
        if (
            import_fields
            and not self.status.game_over
            and (result := search(r"\[Result \"(.+?)\"\]", pgn))
        ):
            match result.group(1):
                case "1/2-1/2":
                    self.draw()
                case "1-0":
                    self._winner = "white"
                    self._game_over = True
                case "0-1":
                    self._winner = "black"
                    self._game_over = True

    def import_fen(self: "ChessBoard", fen: str) -> None:
        """Import Forsyth-Edwards Notation to board."""
        if match := search(
            r"(?P<R8>[^/]+)/(?P<R7>[^/]+)/(?P<R6>[^/]+)/(?P<R5>[^/]+)/"
            r"(?P<R4>[^/]+)/(?P<R3>[^/]+)/(?P<R2>[^/]+)/(?P<R1>[^/\s]+) "
            r"(?P<turn>[wb]) (?P<castling>[KQkqA-Ha-h-]+) (?P<enpassant>[a-h1-8-]+)"
            r"(?: (?P<halfmove>\d+) (?P<fullmove>\d+))?",
            fen,
        ):
            groups = match.groups()
        else:
            msg = "Could not read FEN."
            raise ValueError(msg)

        # Populate board.
        for rank, group in list(zip(range(8, 0, -1), groups[:8], strict=True)):
            cursor = f"a{rank}"
            for char in group:
                if char.isalpha():
                    self[cursor] = FEN_REPRESENTATIONS[char]
                    with suppress(IndexError):
                        cursor = f"{FILES[FILES.index(cursor[0]) + 1]}{cursor[1]}"
                elif char.isnumeric():
                    for _ in range(int(char)):
                        self[cursor] = None
                        with suppress(IndexError):
                            cursor = f"{FILES[FILES.index(cursor[0]) + 1]}{cursor[1]}"

        # Set turn.
        self.turn = "white" if groups[8] == "w" else "black"

        # Set en passant target square.
        if groups[10] != "-":
            self.double_forward_last_move = (
                f"{groups[10][0]}{5 if groups[10][1] == 6 else 4}"
            )

        # Set halfmove clock.
        if groups[11] is not None:
            self.halfmove_clock = int(groups[11])

        # Set fullmove number.
        if groups[12] is not None:
            self.moves_before_fen_import = int(groups[12]) - 1
            if groups[8] == "b":
                self.moves.append("_")

        # Set initial position variables for rooks and kings.
        self.set_initial_positions()

        # Set castling availability.
        if groups[9] == "-":
            self.white_king_has_moved = True
            self.black_king_has_moved = True
        else:
            if self.white_queenside_rook_init_sq is not None:
                queenside_rook_file = self.white_queenside_rook_init_sq[0]
            else:
                queenside_rook_file = "q"
            if self.white_kingside_rook_init_sq is not None:
                kingside_rook_file = self.white_kingside_rook_init_sq[0]
            else:
                kingside_rook_file = "k"
            if "K" not in groups[9] and kingside_rook_file.upper() not in groups[9]:
                self.white_kingside_rook_has_moved = True
            if "Q" not in groups[9] and queenside_rook_file.upper() not in groups[9]:
                self.white_queenside_rook_has_moved = True
            if "k" not in groups[9] and kingside_rook_file not in groups[9]:
                self.black_kingside_rook_has_moved = True
            if "q" not in groups[9] and queenside_rook_file not in groups[9]:
                self.black_queenside_rook_has_moved = True

        self.initial_fen = fen

    @property
    def fen(self: "ChessBoard") -> str:
        """Export the board in Forsyth-Edwards Notation."""
        return self.export_fen()

    def export_fen(self: "ChessBoard", *, no_clocks: bool = False) -> str:
        """Export the board in Forsyth-Edwards Notation."""
        fen = ""

        # Concatenate piece placement data.
        for rank in range(8, 0, -1):
            squares = [f"{file}{rank}" for file in FILES]
            blank_sq_counter = 0
            for sq in squares:
                if self[sq] is None:
                    blank_sq_counter += 1
                    continue
                if blank_sq_counter > 0:
                    fen += str(blank_sq_counter)
                    blank_sq_counter = 0
                piece = self[sq]
                assert piece is not None
                char = PLAINTEXT_ABBRS[piece.piece_type]
                fen += char.upper() if piece.color == "white" else char.lower()
            if blank_sq_counter > 0:
                fen += str(blank_sq_counter)
            if rank > 1:
                fen += "/"

        # Concatenate active color.
        fen += f" {self.turn[0]} "

        # Concatenate castling availability.
        if (
            self.white_king_init_sq is None
            or self.black_king_init_sq is None
            or self.white_kingside_rook_init_sq is None
            or self.white_queenside_rook_init_sq is None
            or self.black_kingside_rook_init_sq is None
            or self.black_queenside_rook_init_sq is None
            or "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" in fen
        ):
            white_kingside_castle_symbol = "K"
            white_queenside_castle_symbol = "Q"
            black_kingside_castle_symbol = "k"
            black_queenside_castle_symbol = "q"
        else:
            white_kingside_castle_symbol = self.white_kingside_rook_init_sq[0].upper()
            white_queenside_castle_symbol = self.white_queenside_rook_init_sq[0].upper()
            black_kingside_castle_symbol = self.black_kingside_rook_init_sq[0]
            black_queenside_castle_symbol = self.black_queenside_rook_init_sq[0]
        any_castles_possible = False
        if not self.white_king_has_moved and not self.white_kingside_rook_has_moved:
            fen += white_kingside_castle_symbol
            any_castles_possible = True
        if not self.white_king_has_moved and not self.white_queenside_rook_has_moved:
            fen += white_queenside_castle_symbol
            any_castles_possible = True
        if not self.black_king_has_moved and not self.black_kingside_rook_has_moved:
            fen += black_kingside_castle_symbol
            any_castles_possible = True
        if not self.black_king_has_moved and not self.black_queenside_rook_has_moved:
            fen += black_queenside_castle_symbol
            any_castles_possible = True
        if not any_castles_possible:
            fen += "-"
        fen += " "

        # Concatenate en passant target square.
        if self.double_forward_last_move is not None:
            fen += self.double_forward_last_move[0]
            if self.double_forward_last_move[1] == "4":
                fen += "3"
            if self.double_forward_last_move[1] == "5":
                fen += "6"
        else:
            fen += "-"

        # Concatenate halfmove and fullmove clocks.
        if not no_clocks:
            fen += (
                f" {self.halfmove_clock} "
                f"{self.moves_before_fen_import + (len(self.moves) // 2) + 1}"
            )

        return fen

    @property
    def pgn(self: "ChessBoard") -> str:
        """Export game in Portable Game Notation."""
        return self.export_pgn()

    def export_pgn(
        self: "ChessBoard",
        event: str | None = None,
        site: str | None = None,
        date: datetime | str | None = None,
        round: str | None = None,
        white: str | None = None,
        black: str | None = None,
        variant: str | None = None,
        *,
        include_current_position: bool = True,
        include_eco: bool = True,
        **kwargs: str,
    ) -> str:
        """Export game in Portable Game Notation."""
        output = ""
        if event is not None:
            output += f'[Event "{event}"]\n'
        elif self._event is not None:
            output += f'[Event "{self._event}"]\n'
        if site is not None:
            output += f'[Site "{site}"]\n'
        elif self._site is not None:
            output += f'[Site "{self._site}"]\n'
        if isinstance(date, datetime):
            date = f"{date.year}.{date.month:02}.{date.day:02}"
        if date is not None:
            output += f'[Date "{date}"]\n'
        elif self._date is not None:
            output += f'[Date "{self._date}"]\n'
        if round is not None:
            output += f'[Round "{round}"]\n'
        elif self._round is not None:
            output += f'[Round "{self._round}"]\n'
        if white is not None:
            output += f'[White "{white}"]\n'
        elif self._white is not None:
            output += f'[White "{self._white}"]\n'
        if black is not None:
            output += f'[Black "{black}"]\n'
        elif self._black is not None:
            output += f'[Black "{self._black}"]\n'
        if not self._game_over:
            output += '[Result "*"]\n'
        elif self._winner is None:
            output += '[Result "1/2-1/2"]\n'
        elif self._winner == "white":
            output += '[Result "1-0"]\n'
        elif self._winner == "black":
            output += '[Result "0-1"]\n'
        if include_eco and (opening := self.get_opening()) is not None:
            output += f'[ECO "{opening.eco}"]\n'
        if variant is not None:
            output += f'[Variant "{variant}"]\n'
        elif self._variant is not None:
            output += f'[Variant "{self._variant}"]\n'
        if self.initial_fen is not None:
            output += f'[FEN "{self.initial_fen}"]\n'
        if include_current_position:
            output += f'[CurrentPosition "{self.fen}"]\n'
        for name, value in self._fields:
            output += f'[{name} "{value}"]\n'
        for key in kwargs:
            key_label = key.title() if key.islower() else key
            output += f'[{key_label} "{kwargs[key]}"]\n'

        output += "\n"
        output += self.export_moves(include_annotations=True)
        return output

    def empty_board(self: "ChessBoard") -> None:
        """Clear all pieces off the board."""
        for key in self:
            self[key] = None
        self.white_king_has_moved = False
        self.white_king_init_sq = None
        self.black_king_has_moved = False
        self.black_king_init_sq = None
        self.black_queenside_rook_has_moved = False
        self.black_queenside_rook_init_sq = None
        self.black_kingside_rook_has_moved = False
        self.black_kingside_rook_init_sq = None
        self.white_queenside_rook_has_moved = False
        self.white_queenside_rook_init_sq = None
        self.white_kingside_rook_has_moved = False
        self.white_kingside_rook_init_sq = None
        self.double_forward_last_move = None
        self.turn = "white"
        self._game_over = False
        self._winner = None
        self.halfmove_clock = 0
        self.moves_before_fen_import = 0
        self.hashes = []
        self.moves = []

    def _get_squares(
        self: "ChessBoard",
        initial_square: str,
        *,
        capture_only: bool = False,
        check_castle: bool = True,
    ) -> Iterator[str]:
        """
        Get all navigable squares for a given piece.
        This includes squares occupied by the king or which, if moved to,
        would put the king in check. Use ChessBoard.legal_moves()
        to only include legal moves.

        If capture_only is True, only include squares which are eligible for capture.
        In other words, pawn forward moves will not be included in return list.

        If check_castle is True, yield post-castling positions for kings.
        """
        if (piece := self[initial_square]) is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        match piece.piece_type:
            case "pawn":
                return self._get_pawn_squares(
                    initial_square, piece, capture_only=capture_only
                )
            case "rook":
                return self._get_rook_squares(initial_square, piece)
            case "queen":
                return self._get_queen_squares(initial_square, piece)
            case "bishop":
                return self._get_bishop_squares(initial_square)
            case "knight":
                return self._get_knight_squares(initial_square)
            case "king":
                return self._get_king_squares(
                    initial_square, piece, check_castle=check_castle
                )

    def legal_moves(self: "ChessBoard", square: str) -> Iterator[str]:
        """Get legal moves for a piece."""
        if (piece := self[square]) is None:
            msg = f"No piece at square '{square}'."
            raise InvalidMoveError(msg)
        for sq in self._get_squares(square):
            # If the piece is a pawn diagonal to the navigable square,
            # and the square at navigable square is None, it must be an en passant.
            if (
                piece.piece_type == "pawn"
                and sq[0] in utils.get_adjacent_files(square)
                and self[sq] is None
            ):
                if self.can_en_passant(square, sq[0]):
                    yield sq
            # If the piece is a king, it could be a castle.
            elif piece.piece_type == "king" and (
                (sq in ("c1", "g1", "c8", "g8") and self.can_castle(piece.color))
                or self.can_move_piece(square, sq)
            ):
                yield sq
            # Otherwise, it goes through move_piece.
            else:
                if self.can_move_piece(square, sq):
                    yield sq

    def can_move_piece(
        self: "ChessBoard",
        initial_square: str,
        final_square: str,
    ) -> bool:
        """
        Check if a piece can be moved to final_square without castling or en passant.
        Does not check turn.
        """
        piece = self[initial_square]
        piece_at_final_square = self[final_square]
        if piece is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        if final_square not in self._get_squares(initial_square):
            return False
        if piece_at_final_square is not None and (
            piece_at_final_square.color == piece.color
            or piece_at_final_square.piece_type == "king"
        ):
            return False
        with self.test_position({final_square: piece, initial_square: None}):
            if self.king_is_in_check(piece.color):
                return False
        return True

    def _get_pawn_squares(
        self: "ChessBoard",
        initial_square: str,
        piece: Piece,
        *,
        capture_only: bool = False,
    ) -> Iterator[str]:
        """Get pawn's navigable squares (ignores king capture rules)."""
        step_func = utils.step_up if piece.color == "white" else utils.step_down
        # forward and double forward advance
        with suppress(utils.OffGridError):
            if not capture_only and self[(sq := step_func(initial_square, 1))] is None:
                yield sq
                starting_rank = "2" if piece.color == "white" else "7"
                if (
                    initial_square[1] == starting_rank
                    and self[(sq := step_func(initial_square, 2))] is None
                ):
                    yield sq
        # diagonal capture
        adjacent_files = utils.get_adjacent_files(initial_square)
        rank = int(initial_square[1])
        for file in adjacent_files:
            sq = f"{file}{rank + 1 if piece.color == 'white' else rank - 1}"
            if sq not in SQUARES:
                break
            if (pc := self[sq]) is not None and pc.color != piece.color:
                yield sq
        # en passant capture
        adjacent_squares = [f"{file}{initial_square[1]}" for file in adjacent_files]
        if self.double_forward_last_move in adjacent_squares:
            yield (
                f"{self.double_forward_last_move[0]}"
                f"{rank + 1 if piece.color == 'white' else rank - 1}"
            )

    def _get_rook_squares(
        self: "ChessBoard", initial_square: str, piece: Piece
    ) -> Iterator[str]:
        """Get rook's navigable squares (ignores king capture rules)."""
        for generator in ROOK_GENERATORS:
            iterator = generator(initial_square)
            for sq in iterator:
                other_piece = self[sq]
                if other_piece is None:
                    yield sq
                else:
                    if other_piece.color != piece.color:
                        yield sq
                    break

    def _get_queen_squares(
        self: "ChessBoard", initial_square: str, piece: Piece
    ) -> Iterator[str]:
        """Get queen's navigable squares (ignores king capture rules)."""
        for generator in QUEEN_GENERATORS:
            for sq in generator(initial_square):
                other_piece = self[sq]
                if other_piece is None:
                    yield sq
                else:
                    if other_piece.color != piece.color:
                        yield sq
                    break

    def _get_bishop_squares(self: "ChessBoard", initial_square: str) -> Iterator[str]:
        """Get bishop navigable squares (ignores king capture rules)."""
        for generator in BISHOP_GENERATORS:
            for sq in generator(initial_square):
                piece = self[sq]
                moving_piece = self[initial_square]
                assert moving_piece is not None
                if piece is None:
                    yield sq
                else:
                    if piece.color != moving_piece.color:
                        yield sq
                    break

    def _get_knight_squares(self: "ChessBoard", initial_square: str) -> Iterator[str]:
        """Get knight navigable squares (ignores king capture rules)."""
        candidates: list[str] = []
        for move in KNIGHT_MOVES:
            with suppress(utils.OffGridError):
                cursor = initial_square
                for direction, steps in move:
                    cursor = STEP_FUNCTIONS_BY_DIRECTION[direction](cursor, steps)
                candidates.append(cursor)
        for sq in candidates:
            piece = self[sq]
            if piece is None:
                yield sq
            else:
                moving_piece = self[initial_square]
                assert moving_piece is not None
                if piece.color != moving_piece.color:
                    yield sq

    def _get_king_squares(
        self: "ChessBoard",
        initial_square: str,
        piece: Piece,
        *,
        check_castle: bool = False,
    ) -> Iterator[str]:
        """Get king navigable squares (ignores capture rules)."""
        for func in STEP_FUNCTIONS_BY_DIRECTION.values():
            with suppress(utils.OffGridError):
                sq = func(initial_square, 1)
                if (pc := self[sq]) is None or pc.color != piece.color:
                    yield sq
        if check_castle:
            if self.can_castle(piece.color, "queenside"):
                yield f"c{initial_square[1]}"
            if self.can_castle(piece.color, "kingside"):
                yield f"g{initial_square[1]}"

    def move_piece(
        self: "ChessBoard",
        initial_square: str,
        final_square: str,
        *,
        autocastle: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
    ) -> None:
        """Move a game piece."""
        notation = ""
        piece = self[initial_square]
        if piece is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        piece_at_final_square = self[final_square]
        # Try to castle if king is moving to a final castling square,
        # or if rook is jumping over a king.
        if (
            autocastle
            and piece.piece_type == "king"
            and final_square in ("c1", "c8", "g1", "g8")
            and self.can_castle(
                piece.color,
                "queenside" if final_square[0] in ("c", "d") else "kingside",
            )
        ):
            self.castle(
                piece.color,
                "queenside" if final_square[0] in ("c", "d") else "kingside",
                skip_checks=True,
            )
            return None
        # Reroute to self.en_passant if pawn captures on empty final square.
        if (
            piece.piece_type == "pawn"
            and initial_square[0] != final_square[0]
            and self[final_square] is None
        ):
            self.en_passant(initial_square, final_square)
            return None
        # Add piece type notation, disambiguating if necessary.
        notation += (
            PLAINTEXT_ABBRS[piece.piece_type] if piece.piece_type != "pawn" else ""
        )
        disambiguator = ""
        ambiguous_pieces = [
            sq
            for sq in self
            if self[sq] == Piece(piece.piece_type, self.turn)
            and sq != initial_square
            and final_square in self.legal_moves(sq)
        ]
        if len(ambiguous_pieces) > 0:
            possible_disambiguators = (
                initial_square[0],
                initial_square[1],
                initial_square,
            )
            for pd in possible_disambiguators:
                ambiguous_pieces = [
                    sq
                    for sq in self
                    if pd in sq
                    and self[sq] == Piece(piece.piece_type, self.turn)
                    and sq != initial_square
                    and final_square in self.legal_moves(sq)
                ]
                if len(ambiguous_pieces) == 0:
                    disambiguator = pd
                    break
        notation += disambiguator
        if not skip_checks:
            # Check correct player's piece is being moved.
            if not ignore_turn and piece.color != self.turn:
                msg = f"It is {self.turn}'s turn."
                raise OtherPlayersTurnError(msg)
            # Check piece can navigate to square.
            if final_square not in self._get_squares(initial_square):
                msg = "Not a valid move."
                raise InvalidMoveError(msg)
        # Update clocks and notation to denote capture, and raise
        # exceptions for illegal captures.
        if piece_at_final_square is not None:
            if piece.piece_type == "pawn" and len(notation) == 0:
                notation += initial_square[0]
            notation += "x"
            is_capture = True
            if piece_at_final_square.color == piece.color:
                msg = "Cannot place piece at square occupied by same color piece."
                raise InvalidMoveError(msg)
            elif piece_at_final_square.piece_type == "king":
                msg = "Cannot capture king."
                raise InvalidMoveError(msg)
        else:
            is_capture = False
        notation += final_square
        # Update has_moved variables (used to determine castling availability).
        if piece.piece_type == "king":
            setattr(self, f"{piece.color}_king_has_moved", True)
        elif piece.piece_type == "rook":
            if initial_square == (
                self.black_kingside_rook_init_sq
                if piece.color == "black"
                else self.white_kingside_rook_init_sq,
            ):
                side: Side | None = "kingside"
            elif initial_square == (
                self.black_queenside_rook_init_sq
                if piece.color == "black"
                else self.white_queenside_rook_init_sq,
            ):
                side = "queenside"
            else:
                side = None
            if side is not None:
                setattr(self, f"{piece.color}_{side}_rook_has_moved", True)
        skip_hash = self.double_forward_last_move is not None
        if (
            piece.piece_type == "pawn"
            and abs(int(initial_square[1]) - int(final_square[1])) == 2
        ):
            self.double_forward_last_move = final_square
        else:
            self.double_forward_last_move = None
        # Test if king would be in check if moved.
        if not skip_checks:
            king_would_be_in_check = False
            with self.test_position({final_square: piece, initial_square: None}):
                if self.king_is_in_check(self.turn):
                    king_would_be_in_check = True
            if king_would_be_in_check:
                msg = "Cannot move piece because king would be in check."
                raise InvalidMoveError(msg)
        self[final_square] = piece
        self[initial_square] = None
        self.alternate_turn(
            reset_halfmove_clock=(piece.piece_type == "pawn" or is_capture),
            skip_hash=skip_hash,
        )
        if self.is_checkmate() is not None:
            notation += "#"
        elif self.king_is_in_check(self.turn):
            notation += "+"
        self.moves.append(notation)

    def submit_moves(self: "ChessBoard", *notations: str) -> None:
        """Submit multiple moves at once with algebraic notation."""
        if len(notations) == 1 and " " in notations[0]:
            notations = tuple(
                sub(
                    r"[\s\n]+",
                    " ",
                    sub(r"\d+\.+|\[.+?\]|\{.+?\}|[10]-[10]|1/2-1/2", "", notations[0]),
                ).split()
            )
        for notation in notations:
            self.move(notation)

    def export_moves(self: "ChessBoard", *, include_annotations: bool = False) -> str:
        """Export moves to string."""
        i = self.moves_before_fen_import
        output = ""
        moves = self.moves
        while True:
            i += 1
            if len(moves) == 1:
                move_no = f"{i}."
                move_annotation = f"{move_no} {moves[0]}"
                output += move_annotation
                if include_annotations and move_no in self._move_annotations:
                    output += f" {{{self._move_annotations[move_no]}}} "
            if len(moves) < 2:
                break
            move_no = f"{i}."
            output += f"{move_no} {moves[0]} "
            if include_annotations and move_no in self._move_annotations:
                output += f"{{{self._move_annotations[move_no]}}} {i}... "
            output += f"{moves[1]} "
            if include_annotations and f"{i}..." in self._move_annotations:
                output += f"{{{self._move_annotations[move_no]}}} "
            moves = moves[2:]
        output = output.strip()
        status = self.status
        if status.game_over:
            match status.winner:
                case "white":
                    output += " 1-0"
                case "black":
                    output += " 0-1"
                case None:
                    output += " 1/2-1/2"
        return sub(r"\. _", "...", output).strip()

    def move(self: "ChessBoard", notation: str) -> None:
        """Make a move using algebraic notation."""
        if "O-O-O" in notation:
            self.castle(self.turn, "queenside")
            return None
        elif "O-O" in notation:
            self.castle(self.turn, "kingside")
            return None
        elif match := search(
            r"([KQRBN]?)([a-h1-8]{,2})x?([a-h][1-8])[\(=/]?([KQRBN]?)\)?\s?.*$",
            notation,
        ):
            piece_type = ALGEBRAIC_PIECE_ABBRS[match.group(1)]
            disambiguator = match.group(2)
            final_square = match.group(3)
            pawn_promotion = (
                ALGEBRAIC_PIECE_ABBRS[grp] if (grp := match.group(4)) != "" else None
            )
            candidates = [
                sq
                for sq in self
                if self[sq] == Piece(piece_type, self.turn)
                and disambiguator in sq
                and final_square in self._get_squares(sq)
            ]
            if len(candidates) == 1:
                initial_square = candidates[0]
            elif len(candidates) == 0:
                msg = f"'{notation}' is not allowed."
                raise InvalidNotationError(msg)
            else:
                successful_candidates = []
                # Test if king would be put in check by move to disambiguate.
                for candidate in candidates:
                    with self.test_position(
                        {
                            candidate: None,
                            final_square: self[candidate],
                        }
                    ):
                        if not self.king_is_in_check(self.turn):
                            successful_candidates.append(candidate)
                if len(successful_candidates) == 1:
                    initial_square = successful_candidates[0]
                elif len(successful_candidates) == 0:
                    msg = f"'{notation}' is not allowed."
                    raise InvalidNotationError(notation)
                else:
                    msg = f"Must disambiguate moving pieces: {candidates}"
                    raise InvalidNotationError(msg)
            if "x" in notation and self[final_square] is None and "#" not in notation:
                with suppress(InvalidMoveError):
                    self.en_passant(initial_square, final_square)
                    return None
            self.move_piece(initial_square, final_square, autocastle=False)
            if pawn_promotion is not None:
                self.promote_pawn(final_square, pawn_promotion)
            return None
        else:
            msg = f"Could not read notation '{notation}'."
            raise InvalidNotationError(msg)

    def can_castle(self: "ChessBoard", color: Color, side: Side | None = None) -> bool:
        """Check if a player can castle. Optionally specify side."""
        # Castling can only be done when:
        #  - The king has not moved.
        #  - The rook has not moved.
        #  - The king is not in check.
        #  - The king would not pass through a checked square.
        #  - The king would not land into a checked square.
        #  - There are no pieces between king and rook.
        king_sq = (
            self.black_king_init_sq if color == "black" else self.white_king_init_sq
        )
        if king_sq is None:
            return False
        king_has_moved_attr = f"{color}_king_has_moved"
        king_has_moved = getattr(self, king_has_moved_attr)
        if king_has_moved:
            return False
        sides = [side] if side is not None else SIDES
        rooks = [
            (
                f"{color}_{side_}_rook_init_sq",
                f"{color}_{side_}_rook_has_moved",
                CASTLING_FINAL_SQUARES[color, side_],
            )
            for side_ in sides
        ]
        rooks = [rook for rook in rooks if rook[0] is not None]
        pcs_allowed_on_final_squares = (
            None,
            Piece("rook", color),
            Piece("king", color),
        )
        for rook_init_sq_attr, rook_has_moved_attr, final_squares in rooks:
            rook_init_sq = getattr(self, rook_init_sq_attr)
            rook_has_moved = getattr(self, rook_has_moved_attr)
            if rook_init_sq is None:
                continue
            squares_between = utils.get_squares_between(king_sq, rook_init_sq)
            squares_king_crosses = utils.get_squares_between(king_sq, final_squares[0])
            if (
                not king_has_moved
                and not rook_has_moved
                and self[rook_init_sq] == Piece("rook", color)
                and all(self[sq] is None for sq in squares_between)
                and all(
                    self[sq] in pcs_allowed_on_final_squares for sq in final_squares
                )
                and not self.king_is_in_check(color)
                and not any(
                    sq in squares_king_crosses for sq in self.checked_squares(color)
                )
            ):
                return True
        return False

    def castle(
        self: "ChessBoard",
        color: Color,
        side: Side,
        *,
        skip_checks: bool = False,
    ) -> None:
        """
        Move the king two spaces right or left and move the closest rook
        to its other side.
        """
        if not skip_checks and color != self.turn:
            msg = f"It is {self.turn.upper()}'s turn."
            raise OtherPlayersTurnError(msg)
        if skip_checks or self.can_castle(color, side):
            king_final_sq, rook_final_sq = CASTLING_FINAL_SQUARES[color, side]
            king_init_sq = getattr(self, f"{color}_king_init_sq")
            rook_init_sq = getattr(self, f"{color}_{side}_rook_init_sq")
            self[king_init_sq] = None
            self[rook_init_sq] = None
            self[king_final_sq] = Piece("king", color)
            self[rook_final_sq] = Piece("rook", color)
            setattr(self, f"{color}_king_has_moved", True)
            setattr(self, f"{color}_{side}_rook_has_moved", True)
            skip_hash = self.double_forward_last_move is not None
            self.double_forward_last_move = None
            self.alternate_turn(skip_hash=skip_hash)
            notation = "O-O" if side == "kingside" else "O-O-O"
            if self.is_checkmate():
                notation += "#"
            elif self.king_is_in_check(self.turn):
                notation += "+"
            self.moves.append(notation)
        else:
            msg = "Castling not allowed."
            raise InvalidMoveError(msg)

    def promote_pawn(self: "ChessBoard", square: str, piece_type: PieceType) -> None:
        """Promote a pawn on the farthest rank from where it started."""
        if (piece := self[square]) is None:
            msg = f"No piece at square '{square}'."
            raise InvalidMoveError(msg)
        if piece.color == self.turn:
            msg = f"It is {self.turn}'s turn."
            raise OtherPlayersTurnError(msg)
        if (piece.color == "white" and square[1] != "8") or (
            piece.color == "black" and square[1] != "1"
        ):
            msg = (
                "Cannot promote pawn unless it is at "
                "farthest rank from where it started."
            )
            raise InvalidMoveError(msg)
        self[square] = Piece(piece_type, piece.color)
        self.double_forward_last_move = None
        updated_notation = f"{self.moves[-1]}={PLAINTEXT_ABBRS[piece_type]}"
        if self.is_checkmate():
            updated_notation = f"{updated_notation.replace('+', '')}#"
        elif self.king_is_in_check(self.turn):
            updated_notation = f"{updated_notation.replace('+', '')}+"
        if "==" in updated_notation:
            updated_notation = f"{updated_notation.replace('==', '=')}="
        self.moves[-1] = updated_notation
        self.hashes.append(hash(self))

    def can_en_passant(
        self: "ChessBoard",
        initial_square: str,
        capture_file: str | None = None,
    ) -> bool:
        """Check if an en passant capture is possible."""
        if self.double_forward_last_move is None:
            return False
        candidate_squares = []
        for func in (utils.step_left, utils.step_right):
            with suppress(utils.OffGridError):
                square = func(initial_square, 1)
                if capture_file is None or capture_file in square:
                    candidate_squares.append(square)
        if self.double_forward_last_move not in candidate_squares:
            return False
        if (piece := self[initial_square]) is None:
            return False
        color = piece.color
        with self.test_position(
            {
                initial_square: None,
                f"{capture_file}{6 if color == 'white' else 3}": Piece("pawn", color),
                self.double_forward_last_move: None,
            }
        ):
            if self.king_is_in_check(color):
                return False
        return True

    def en_passant(
        self: "ChessBoard",
        initial_square: str,
        final_square: str,
        *,
        skip_checks: bool = False,
    ) -> None:
        """Capture an adjacent file pawn that has just made a double forward advance."""
        piece = self[initial_square]
        if not skip_checks:
            if piece is None:
                msg = f"No piece at initial_square '{initial_square}'."
                raise InvalidMoveError(msg)
            if piece.color != self.turn:
                msg = f"It is {self.turn}'s turn."
                raise OtherPlayersTurnError(msg)
        assert piece is not None
        if skip_checks or self.can_en_passant(initial_square, final_square[0]):
            assert self.double_forward_last_move is not None
            self[self.double_forward_last_move] = None
            self[initial_square] = None
            self[final_square] = piece
            self.double_forward_last_move = None
            notation = f"{initial_square[0]}x{final_square}"
            self.alternate_turn(reset_halfmove_clock=True, skip_hash=True)
            if self.is_checkmate():
                notation += "#"
            elif self.king_is_in_check(self.turn):
                notation += "+"
            self.moves.append(notation)

    @property
    def pieces(self: "ChessBoard") -> dict[str, Piece]:
        """Get all pieces on the board."""
        return {sq: piece for sq in self.grid if (piece := self[sq]) is not None}

    def checked_squares(self: "ChessBoard", color: Color) -> list[str]:
        """Get all checked squares for a color."""
        other_color = "white" if color == "black" else "black"
        other_color_pieces = [
            sq
            for sq in self
            if (pc := self[sq]) is not None and pc.color == other_color
        ]
        checked_squares: list[str] = []
        for sq in other_color_pieces:
            checked_squares.extend(
                self._get_squares(sq, capture_only=True, check_castle=False)
            )
        return checked_squares

    def is_checkmate(self: "ChessBoard") -> str | None:
        """
        Check if either color's king is checkmated.
        Returns winning color or None.
        """
        kings = [
            (sq, pc)
            for sq in self
            if (pc := self[sq]) is not None and pc.piece_type == "king"
        ]
        for sq, king in kings:
            if (
                self.king_is_in_check(king.color)
                and not self.can_block_check(king.color)
                and len(list(self.legal_moves(sq))) == 0
            ):
                self._game_over = True
                self._winner = "black" if king.color == "white" else "white"
                self._status_description = "checkmate"
                return self._winner
        return None

    @property
    def status(self: "ChessBoard") -> GameStatus:
        """Check the board for a checkmate or draw."""
        if self._game_over:
            return GameStatus(self._game_over, self._winner, self._status_description)
        if self.is_checkmate():
            return GameStatus(
                game_over=True,
                winner=self._winner,
                description=self._status_description,
            )
        # Check for stalemate.
        pieces = self.pieces
        squares = [sq for sq in pieces if pieces[sq].color == self.turn]
        possible_squares: list[str] = []
        for sq in squares:
            possible_squares.extend(self.legal_moves(sq))
        if len(possible_squares) == 0 and not self.can_castle(self.turn):
            self._game_over = True
            self._status_description = "stalemate"
            return GameStatus(game_over=True, description=self._status_description)
        # Check for draw by repetition.
        with suppress(IndexError):
            if Counter(self.hashes).most_common(1)[0][1] >= 5:
                self._game_over = True
                self._status_description = "fivefold_repetition"
                return GameStatus(game_over=True, description=self._status_description)
        # Check for draw by insufficient material.
        is_sufficient = False
        white_pieces = []
        black_pieces = []
        for sq in pieces:
            if (pc := pieces[sq]).color == "white":
                white_pieces.append(pc.piece_type)
            else:
                black_pieces.append(pc.piece_type)
        for color in COLORS:
            if color == "white":
                color_pieces = white_pieces
                other_color_pieces = black_pieces
            else:
                color_pieces = black_pieces
                other_color_pieces = white_pieces
            # A king + any(pawn, rook, queen) is sufficient.
            if (
                "rook" in color_pieces
                or "pawn" in color_pieces
                or "queen" in color_pieces
            ):
                is_sufficient = True
                break
            # A king and more than one other type of piece is sufficient
            # (i.e. knight + bishop). A king and two (or more) knights
            # is also sufficient.
            if color_pieces.count("knight") + color_pieces.count("bishop") > 1:
                is_sufficient = True
                break
            # King + knight against king + any(rook, bishop, knight, pawn)
            # is sufficient.
            if "knight" in color_pieces and any(
                pt in other_color_pieces for pt in ("rook", "knight", "bishop", "pawn")
            ):
                is_sufficient = True
                break
            # King + bishop against king + any(knight, pawn) is sufficient.
            if "bishop" in color_pieces and (
                "knight" in other_color_pieces or "pawn" in other_color_pieces
            ):
                is_sufficient = True
                break
            # King + bishop(s) is also sufficient if there's bishops on
            # opposite colours (even king + bishop against king + bishop).
            if "bishop" in color_pieces and "bishop" in other_color_pieces:
                bishops = [sq for sq in pieces if pieces[sq].piece_type == "bishop"]
                bishop_square_colors = {
                    ("white" if bishop in WHITE_SQUARES else "black")
                    for bishop in bishops
                }
                if len(bishop_square_colors) == 2:
                    is_sufficient = True
                    break
        if not is_sufficient:
            self._game_over = True
            self._status_description = "insufficient_material"
            return GameStatus(game_over=True, description=self._status_description)
        # Check for draw by 75 moves without capture.
        if self.halfmove_clock >= 150:
            self._game_over = True
            self._status_description = "the_75_move_rule"
            return GameStatus(game_over=True, description=self._status_description)
        self._game_over = False
        return GameStatus(game_over=False)

    def can_block_check(self: "ChessBoard", color: Color) -> bool:
        """Return True if a check can be blocked by another piece."""
        pieces = self.pieces
        same_color_pieces = []
        other_color_pieces = []
        for sq in pieces:
            if pieces[sq].color == color:
                same_color_pieces.append(sq)
            else:
                other_color_pieces.append(sq)
        king: str = next(
            sq for sq in same_color_pieces if pieces[sq].piece_type == "king"
        )
        same_color_pieces_except_king = [
            sq for sq in same_color_pieces if pieces[sq].piece_type != "king"
        ]
        checks: list[str] = [
            piece
            for piece in other_color_pieces
            if king in self._get_squares(piece, capture_only=True)
        ]
        squares_that_would_block_check = []
        for check in checks:
            if (rank_difference := int(king[1]) - int(check[1])) > 0:
                rank_direction = "up"  # i.e. king is upward of piece
            elif rank_difference == 0:
                rank_direction = "inline"
            else:
                rank_direction = "down"
            if (file_difference := FILES.index(king[0]) - FILES.index(check[0])) > 0:
                file_direction = "right"  # i.e. king is to the right of piece
            elif file_difference == 0:
                file_direction = "inline"
            else:
                file_direction = "left"
            possible_squares = [
                check,
                *list(DIRECTION_GENERATORS[rank_direction, file_direction](check)),
            ]
            if (pt := pieces[check].piece_type) in ("knight", "pawn"):
                squares_that_would_block_check.append(check)
            if pt in ("rook", "bishop", "queen"):
                for square in possible_squares:
                    if square == king:
                        break
                    squares_that_would_block_check.append(square)
        possible_moves: list[tuple[str, str]] = []  # [(from, to), ...]
        for sq in same_color_pieces_except_king:
            possible_moves.extend([(sq, move) for move in self._get_squares(sq)])
        # Check if en passant capture can block check.
        if self.double_forward_last_move is not None:
            adjacent_squares = [
                f"{file}{self.double_forward_last_move[1]}"
                for file in utils.get_adjacent_files(self.double_forward_last_move)
            ]
            final_rank = (
                int(self.double_forward_last_move[1]) + 1
                if color == "white"
                else int(self.double_forward_last_move[1]) - 1
            )
            final_sq = f"{self.double_forward_last_move[0]}{final_rank}"
            for sq in adjacent_squares:
                if self[sq] == Piece("pawn", color) and self.can_en_passant(
                    sq, self.double_forward_last_move[0]
                ):
                    with self.test_position(
                        {
                            self.double_forward_last_move: None,
                            sq: None,
                            final_sq: Piece("pawn", color),
                        }
                    ):
                        if not self.king_is_in_check(color):
                            return True
        squares_that_can_be_moved_to = [move[1] for move in possible_moves]
        for square in squares_that_can_be_moved_to:
            if square in squares_that_would_block_check:
                candidates = [move for move in possible_moves if move[1] == square]
                for initial_sq, final_sq in candidates:
                    with self.test_position(
                        {
                            initial_sq: None,
                            final_sq: self[initial_sq],
                        }
                    ):
                        if not self.king_is_in_check(color):
                            return True
        return False

    def king_is_in_check(self: "ChessBoard", color: Color) -> bool | None:
        """Return True if king is in check."""
        try:
            king_sq = next(sq for sq in self.pieces if self[sq] == Piece("king", color))
        except StopIteration:
            return None
        # Find the squares which, if occupied by an opposite color pawn, check the king.
        pawn_sq_funcs = (
            (utils.step_diagonal_up_left, utils.step_diagonal_up_right)
            if color == "white"
            else (utils.step_diagonal_down_left, utils.step_diagonal_down_right)
        )
        pawn_sqs = []
        for func in pawn_sq_funcs:
            with suppress(utils.OffGridError):
                pawn_sqs.append(func(king_sq, 1))
        for sq in pawn_sqs:
            if self[sq] == Piece("pawn", "white" if color == "black" else "black"):
                return True
        # Check if opposite color king is touching the king.
        for func_ in STEP_FUNCTIONS_BY_DIRECTION.values():
            try:
                sq = func_(king_sq, 1)
            except utils.OffGridError:
                continue
            if self[sq] == Piece("king", "black" if color == "white" else "white"):
                return True
        # Check if a piece above/left/right/below king can capture.
        for generator in ROOK_GENERATORS:
            for sq in generator(king_sq):
                if (
                    (pc := self[sq]) is not None
                    and pc.color != color
                    and pc.piece_type in ("rook", "queen")
                ):
                    return True
                elif pc is not None:
                    break
        # Check if a piece diagonal to king can capture.
        for generator in BISHOP_GENERATORS:
            for sq in generator(king_sq):
                if (
                    (pc := self[sq]) is not None
                    and pc.color != color
                    and pc.piece_type in ("bishop", "queen")
                ):
                    return True
                elif pc is not None:
                    break
        # Check if an opponent knight checks the king.
        with self.test_position({king_sq: Piece("knight", color)}):
            for sq in self._get_knight_squares(king_sq):
                if self[sq] == Piece(
                    "knight", "black" if color == "white" else "white"
                ):
                    return True
        return False

    def resign(self: "ChessBoard", color: Color | None = None) -> GameStatus:
        """Resign instead of moving."""
        self._game_over = True
        if color is None:
            self._winner = "white" if self.turn == "black" else "black"
        else:
            self._winner = "white" if color == "black" else "black"
        self._status_description = "opponent_resignation"
        return GameStatus(self._game_over, self._winner, self._status_description)

    def draw(self: "ChessBoard") -> GameStatus:
        """Draw instead of moving."""
        if self.can_claim_draw():
            return self.claim_draw()
        self._game_over = True
        self._winner = None
        return GameStatus(game_over=True, description="agreement")

    def can_claim_draw(self: "ChessBoard") -> bool:
        """Check if a draw can be claimed without agreement."""
        return (
            self.can_claim_draw_by_halfmove_clock()
            or self.can_claim_draw_by_threefold_repetition()
        )

    def can_claim_draw_by_halfmove_clock(self: "ChessBoard") -> bool:
        """Check if draw can be claimed due to 50 moves without pawn move or capture."""
        return self.halfmove_clock >= 100

    def can_claim_draw_by_threefold_repetition(self: "ChessBoard") -> bool:
        """Check if draw can be claimed due to threefold repetition."""
        try:
            return Counter(self.hashes).most_common(1)[0][1] >= 3
        except IndexError:
            return False

    def claim_draw(self: "ChessBoard") -> GameStatus:
        """Claim a draw due to 50 moves without a capture or pawn move."""
        if self._game_over:
            return GameStatus(self._game_over, self._winner, self._status_description)
        if self.halfmove_clock >= 100:
            self._game_over = True
            self._winner = None
            self._status_description = "the_50_move_rule"
            return GameStatus(game_over=True, description=self._status_description)
        if Counter(self.hashes).most_common(1)[0][1] >= 3:
            self._game_over = True
            self._winner = None
            self._status_description = "threefold_repetition"
            return GameStatus(game_over=True, description=self._status_description)
        return GameStatus(game_over=False)

    @property
    def rich_renderable(self: "ChessBoard") -> str:
        """Return a Rich renderable representation of the board."""
        rank_renderable = "\n"
        for rank in range(8, 0, -1):
            rank_renderable += f"[white]{rank}[/white] "
            rank_grid = [sq for sq in self if sq[1] == str(rank)]
            for sq in rank_grid:
                piece = self[sq]
                if piece is not None:
                    if piece.color == "white":
                        rank_renderable += (
                            f"[reverse][#ffffff]{PIECE_SYMBOLS[piece.piece_type]} "
                            "[/#ffffff][/reverse]"
                        )
                    else:
                        rank_renderable += (
                            f"[white]{PIECE_SYMBOLS[piece.piece_type]} [/white]"
                        )
                else:
                    if sq in BLACK_SQUARES:
                        rank_renderable += "[reverse][#789656]  [/reverse][/#789656]"
                    else:
                        rank_renderable += "[reverse][#f0edd1]  [/reverse][/#f0edd1]"
            rank_renderable += "\n"
        rank_renderable += "[bold][white]  a b c d e f g h [/bold][/white]\n"
        return rank_renderable

    @property
    def ascii_repr(self: "ChessBoard") -> str:
        """Get an ASCII representation of the board."""
        output = ""
        for rank in range(8, 0, -1):
            output += f"{rank} "
            rank_grid = [sq for sq in self if sq[1] == str(rank)]
            for sq in rank_grid:
                piece = self[sq]
                if piece is None:
                    output += ". "
                else:
                    char = (
                        PLAINTEXT_ABBRS[piece.piece_type].upper()
                        if piece.color == "white"
                        else PLAINTEXT_ABBRS[piece.piece_type].lower()
                    )
                    output += f"{char} "
            output += "\n"
        output += "  a b c d e f g h "
        return output

    def print(self: "ChessBoard", *, plaintext: bool = False) -> None:
        """Print the ChessBoard to console."""
        if not plaintext and "Console" in globals():
            Console().print(self.rich_renderable)
        else:
            print(self.ascii_repr)
