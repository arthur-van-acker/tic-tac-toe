"""Main entry point for the Tic Tac Toe application."""

import sys


def main():
    """Entry point for the application."""
    # TODO: Add argument parsing for UI selection
    # For now, default to GUI
    from tictactoe.ui.gui.main import main as gui_main

    gui_main()


if __name__ == "__main__":
    sys.exit(main())
