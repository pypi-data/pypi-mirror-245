"""A game of chess in the console."""

from sys import argv

from rich.console import Console
from rich.prompt import Prompt
from rich.rule import Rule

try:
    from consolechess.board import ChessBoard
except ImportError:
    from board import ChessBoard  # type: ignore


def main() -> None:
    """Start a game of chess in the terminal."""
    console = Console()
    board = ChessBoard()
    if "random" in argv:
        board.set_random()
    result = None
    while result is None:
        board.print()
        console.print(Rule())
        if board.turn == "white":
            console.print("[reverse][bold]WHITE[/bold][/reverse] to move.")
        else:
            console.print("[bold]BLACK[/bold] to move.")
        console.print(
            "\n[b]Enter your move in algrebraic chess notation.[/b]\n"
            "Enter 'draw' to offer draw.\nEnter 'resign' to resign.\n"
        )
        move = Prompt.ask("Enter your move")
        if move == "resign":
            board.print()
            board.resign()
            result = board.status
            if result.winner == "white":
                console.print("[bold][reverse]WHITE[/reverse][/bold] won the game.")
            elif result.winner == "black":
                console.print("[bold]BLACK[/bold] won the game.")
            print(f"Moves: {board.export_moves()}\n")
        elif move == "draw":
            response = Prompt.ask(
                "[bold]"
                f"{'[reverse]WHITE[/reverse]' if board.turn == 'white' else 'BLACK'}"
                "[/bold] offered a draw. Does "
                f"{'[reverse]WHITE[/reverse]' if board.turn == 'black' else 'BLACK'}"
                " accept?",
                choices=["yes", "no"],
            )
            print("\n")
            if response == "yes":
                board.print()
                console.print("The game ended in a [bold]DRAW[/bold].")
                board.draw()
                print(f"Moves: {board.export_moves()}\n")
                result = board.status
        else:
            try:
                board.move(move)
            except Exception as exc:
                console.print(f"\n[red]{exc}[/red]\n")
            if board._game_over:
                board.print()
                result = board.status
                if result.winner == "white":
                    console.print("[bold][reverse]WHITE[/reverse][/bold] won the game.")
                elif result.winner == "black":
                    console.print("[bold]BLACK[/bold] won the game.")
                else:
                    console.print("The game ended in a [bold]DRAW[/bold].")
                print(f"Moves: {board.export_moves()}\n")


if __name__ == "__main__":
    main()
