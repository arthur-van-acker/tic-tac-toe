"""GUI implementation for Tic Tac Toe using CustomTkinter."""

from tictactoe.domain.logic import GameSnapshot, TicTacToe
from tictactoe.ui.gui import bootstrap
from tictactoe.ui.gui.theme import apply_default_theme
from tictactoe.ui.gui.view import GameView


bootstrap.configure_windows_app_model()


class TicTacToeGUI:
    """Main GUI application for Tic Tac Toe."""

    def __init__(self):
        """Initialize the GUI application."""
        self.game = TicTacToe()
        self._ctk_env = bootstrap.load_customtkinter()
        self.ctk = self._ctk_env.module
        self._ctk_headless = self._ctk_env.headless
        self.root = self._create_root()

        self.root.title("Tic Tac Toe")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        apply_default_theme(self.ctk)

        self.icon_path = bootstrap.locate_icon_file()
        bootstrap.apply_window_icon(
            self.root, self.icon_path, headless=self._ctk_headless
        )

        self.view = GameView(
            ctk_module=self.ctk,
            root=self.root,
            on_cell_click=self._on_cell_click,
            on_reset=self._reset_game,
        )
        self.view.build()
        self._expose_view_handles()

        self.game.add_listener(self._on_game_updated)
        self._on_game_updated(self.game.snapshot)

    def _create_root(self):
        """Create the root window with fallback to headless widgets."""

        module, root, env = bootstrap.create_root(self._ctk_env)
        self.ctk = module
        self._ctk_env = env
        self._ctk_headless = env.headless
        return root

    def _expose_view_handles(self) -> None:
        """Expose view widgets for tests and legacy callers."""

        self.title_label = self.view.title_label
        self.status_label = self.view.status_label
        self.board_frame = self.view.board_frame
        self.reset_button = self.view.reset_button
        self.buttons = self.view.buttons

    def _on_cell_click(self, position: int):
        """Handle cell button click."""
        self.game.make_move(position)

    def _on_game_updated(self, snapshot: GameSnapshot) -> None:
        """Render the latest game snapshot to the UI widgets."""

        if not hasattr(self, "buttons"):
            return

        self.view.render(snapshot)

    def _reset_game(self):
        """Reset the game to initial state."""
        self.game.reset()

    def run(self):
        """Start the GUI application."""
        # Set icon after everything is initialized (CustomTkinter workaround)
        bootstrap.schedule_icon_refresh(
            self.root, self.icon_path, headless=self._ctk_headless
        )
        self.root.mainloop()


def main():
    """Entry point for the GUI application."""
    app = TicTacToeGUI()
    app.run()


if __name__ == "__main__":
    main()
