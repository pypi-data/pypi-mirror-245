"""Play a game of chess in Python module mode, i.e. `python -m chess`."""

from sys import argv

try:
    from consolechess import console, tui
except ImportError:
    import console  # type: ignore
    import tui  # type: ignore


def main() -> None:
    """Start chess."""
    if "console" in argv or "-c" in argv or "--console" in argv:
        console.main()
    else:
        tui.main()


if __name__ == "__main__":
    main()
