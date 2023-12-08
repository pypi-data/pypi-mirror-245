"""Play a game of chess in Python module mode, i.e. `python -m chess`."""

from sys import argv

try:
    from consolechess import asciiconsole, console, tui
except ImportError:
    import asciiconsole  # type: ignore
    import console  # type: ignore
    import tui  # type: ignore


def main() -> None:
    """Start chess."""
    args = " ".join(argv)
    if "ascii" in args:
        asciiconsole.main()
    elif "console" in args or "-c" in args:
        console.main()
    else:
        tui.main()


if __name__ == "__main__":
    main()
