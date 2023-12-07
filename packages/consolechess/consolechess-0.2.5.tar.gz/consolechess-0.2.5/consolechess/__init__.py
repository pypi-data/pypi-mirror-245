"""A game of chess."""

try:
    from consolechess.board import ChessBoard, Piece
except ImportError:
    from board import ChessBoard, Piece  # type: ignore # noqa: F401
