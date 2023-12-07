"""Helper functions for board.py."""

from collections.abc import Iterator
from contextlib import suppress
from pathlib import Path
from typing import Literal

FILES = list("abcdefgh")
SQUARES = [f"{file}{rank}" for rank in range(1, 9) for file in FILES]

PieceType = Literal["king", "queen", "rook", "bishop", "knight", "pawn"]
Color = Literal["white", "black"]
Side = Literal["kingside", "queenside"]


class OffGridError(Exception):
    """Raised when a square does not exist."""


def get_adjacent_files(square: str) -> list[str]:
    """Get FILES adjacent to square."""
    adjacent_files: list[str] = []
    match square[0]:
        case "a":
            adjacent_files = ["b"]
        case "h":
            adjacent_files = ["g"]
        case _:
            for index in (
                FILES.index(square[0]) + 1,
                FILES.index(square[0]) - 1,
            ):
                with suppress(IndexError):
                    adjacent_files.append(FILES[index])
    return adjacent_files


def iter_to_top(square: str) -> Iterator[str]:
    """Get board squares up to the top (rank 8)."""
    for rank in range(int(square[1]) + 1, 9):
        yield f"{square[0]}{rank}"


def iter_to_bottom(square: str) -> Iterator[str]:
    """Get board squares down to the bottom (rank 1)."""
    for rank in range(int(square[1]) - 1, 0, -1):
        yield f"{square[0]}{rank}"


def iter_to_right(square: str) -> Iterator[str]:
    """Get board squares to the right (file h)."""
    for file in FILES[FILES.index(square[0]) + 1 :]:
        yield f"{file}{square[1]}"


def iter_to_left(square: str) -> Iterator[str]:
    """Get board squares to the left (file a)."""
    for file in reversed(FILES[: FILES.index(square[0])]):
        yield f"{file}{square[1]}"


def iter_top_right_diagonal(square: str) -> Iterator[str]:
    """Get board squares diagonally upward and to the right from square."""
    for file, rank in zip(
        FILES[FILES.index(square[0]) + 1 :],
        range(int(square[1]) + 1, 9),
        strict=False,
    ):
        yield f"{file}{rank}"


def iter_bottom_left_diagonal(square: str) -> Iterator[str]:
    """Get board squares diagonally downward and to the left from square."""
    for file, rank in zip(
        reversed(FILES[: FILES.index(square[0])]),
        range(int(square[1]) - 1, 0, -1),
        strict=False,
    ):
        yield f"{file}{rank}"


def iter_top_left_diagonal(square: str) -> Iterator[str]:
    """Get board squares diagonally upward and to the left from square."""
    for file, rank in zip(
        reversed(FILES[: FILES.index(square[0])]),
        range(int(square[1]) + 1, 9),
        strict=False,
    ):
        yield f"{file}{rank}"


def iter_bottom_right_diagonal(square: str) -> Iterator[str]:
    """Get board squares diagonally downward and to the right from square."""
    for file, rank in zip(
        FILES[FILES.index(square[0]) + 1 :],
        range(int(square[1]) - 1, 0, -1),
        strict=False,
    ):
        yield f"{file}{rank}"


def step_up(square: str, steps: int) -> str:
    """
    Get square `steps` up from `square`.

    Raises
    ------
        OffGrid - when square does not exist.
    """
    rank = int(square[1]) + steps
    if rank > 0 and rank < 9:
        return f"{square[0]}{rank}"
    else:
        msg = "The square does not exist."
        raise OffGridError(msg)


def step_down(square: str, steps: int) -> str:
    """
    Get square `steps` down from `square`.

    Raises
    ------
        OffGrid - when square does not exist.
    """
    rank = int(square[1]) - steps
    if rank > 0 and rank < 9:
        return f"{square[0]}{rank}"
    else:
        msg = "The square does not exist."
        raise OffGridError(msg)


def step_right(square: str, steps: int) -> str:
    """
    Get square `steps` right from `square`.

    Raises
    ------
        OffGrid - when square does not exist.
    """
    col_index = FILES.index(square[0]) + steps
    if col_index >= 0 and col_index <= 7:
        return f"{FILES[col_index]}{square[1]}"
    else:
        msg = "The square does not exist."
        raise OffGridError(msg)


def step_left(square: str, steps: int) -> str:
    """
    Get square `steps` left from `square`.

    Raises
    ------
        OffGrid - when square does not exist.
    """
    col_index = FILES.index(square[0]) - steps
    if col_index >= 0 and col_index <= 7:
        return f"{FILES[col_index]}{square[1]}"
    else:
        msg = "The square does not exist."
        raise OffGridError(msg)


def step_diagonal_up_right(square: str, steps: int) -> str:
    """Step diagonally to the top and right from square."""
    cursor = square
    for _ in range(steps):
        cursor = step_up(cursor, 1)
        cursor = step_right(cursor, 1)
    return cursor


def step_diagonal_up_left(square: str, steps: int) -> str:
    """Step diagonally to the top and left from square."""
    cursor = square
    for _ in range(steps):
        cursor = step_up(cursor, 1)
        cursor = step_left(cursor, 1)
    return cursor


def step_diagonal_down_right(square: str, steps: int) -> str:
    """Step diagonally to the bottom and right from square."""
    cursor = square
    for _ in range(steps):
        cursor = step_down(cursor, 1)
        cursor = step_right(cursor, 1)
    return cursor


def step_diagonal_down_left(square: str, steps: int) -> str:
    """Step diagonally to the bottom and left from square."""
    cursor = square
    for _ in range(steps):
        cursor = step_down(cursor, 1)
        cursor = step_left(cursor, 1)
    return cursor


def get_squares_between(
    square_1: str, square_2: str, *, strict: bool = False
) -> list[str]:
    """
    Get the squares between two other squares on the board.

    Squares must be directly horizontal, vertical, or diagonal
    to each other.

    Raises
    ------
    ValueError - if squares are not inline.
    """
    if square_1 == square_2:
        return []
    if square_1[0] == square_2[0] and square_1[1] != square_2[1]:
        if int(square_1[1]) < int(square_2[1]):
            iterator = iter_to_top
        else:
            iterator = iter_to_bottom
    elif square_1[0] != square_2[0] and square_1[1] == square_2[1]:
        if FILES.index(square_1[0]) < FILES.index(square_2[0]):
            iterator = iter_to_right
        else:
            iterator = iter_to_left
    elif square_1[0] != square_2[0] and square_1[1] != square_2[1]:
        if int(square_1[1]) < int(square_2[1]) and FILES.index(
            square_1[0]
        ) < FILES.index(square_2[0]):
            iterator = iter_top_right_diagonal
        elif int(square_1[1]) < int(square_2[1]):
            iterator = iter_top_left_diagonal
        elif int(square_1[1]) > int(square_2[1]) and FILES.index(
            square_1[0]
        ) < FILES.index(square_2[0]):
            iterator = iter_bottom_right_diagonal
        else:
            iterator = iter_bottom_left_diagonal
    squares_between = []
    met_square_2 = False
    for sq in iterator(square_1):
        if sq == square_2:
            met_square_2 = True
            break
        squares_between.append(sq)
    if met_square_2:
        return squares_between
    else:
        if strict:
            msg = (
                "Squares must be directly diagonal, horizontal,"
                "or vertical to each other."
            )
            raise ValueError(msg)
        else:
            return []


def read_pgn_database(path: str | Path) -> list[str]:
    """Read a .pgn file to a list of PGN strings."""
    if not isinstance(path, Path):
        path = Path(path)
    with path.open() as file:
        text = file.read()
    pgns = text.split("\n\n[")
    pgns = [f"[{pgn}" for pgn in pgns if pgn[0] != "["]
    return pgns
