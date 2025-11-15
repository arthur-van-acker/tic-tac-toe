"""GUI implementation for Tic Tac Toe using CustomTkinter."""

from pathlib import Path
import os
import sys
from tkinter import TclError

from tictactoe.domain.logic import TicTacToe, GameState


def _load_customtkinter(force_headless: bool = False):
    """Load CustomTkinter or fall back to headless stubs."""
    if force_headless or os.environ.get("TICTACTOE_HEADLESS") == "1":
        from tictactoe.ui.gui import headless as headless_ctk

        return headless_ctk, True

    try:
        import customtkinter as real_ctk

        return real_ctk, False
    except Exception:
        from tictactoe.ui.gui import headless as headless_ctk

        return headless_ctk, True


ctk, IS_HEADLESS = _load_customtkinter()

# Fix taskbar icon on Windows
import platform
if platform.system() == "Windows":
    try:
        import ctypes
        # Set AppUserModelID to make Windows treat this as a separate app
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("TicTacToe.Game.v0.1.0")
    except:
        pass


class TicTacToeGUI:
    """Main GUI application for Tic Tac Toe."""

    def __init__(self):
        """Initialize the GUI application."""
        self.game = TicTacToe()
        self._ctk_headless = IS_HEADLESS
        self.root = self._create_root()
        
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Set icon - try multiple paths for different installation scenarios
        possible_paths = [
            Path(__file__).parent.parent.parent / "assets" / "favicon.ico",  # Development
            Path(sys.prefix) / "Lib" / "site-packages" / "tictactoe" / "assets" / "favicon.ico",  # Installed
        ]
        
        self.icon_path = None
        for path in possible_paths:
            if path.exists():
                self.icon_path = path
                break
        
        if self.icon_path and not self._ctk_headless:
            try:
                # Set icon for window and taskbar
                self.root.iconbitmap(default=str(self.icon_path))
            except Exception as e:
                print(f"Warning: Could not set icon: {e}")
        else:
            print("Warning: Icon file not found")
        
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create UI elements
        self._create_widgets()
        
    def _create_root(self):
        """Create the root window with fallback to headless widgets."""
        global ctk, IS_HEADLESS
        try:
            return ctk.CTk()
        except TclError:
            if not IS_HEADLESS:
                ctk, IS_HEADLESS = _load_customtkinter(force_headless=True)
                self._ctk_headless = True
                return ctk.CTk()
            raise

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Title
        self.title_label = ctk.CTkLabel(
            self.root,
            text="Tic Tac Toe",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.root,
            text=f"Player {self.game.current_player.value}'s turn",
            font=ctk.CTkFont(size=20)
        )
        self.status_label.pack(pady=10)
        
        # Game board frame
        self.board_frame = ctk.CTkFrame(self.root)
        self.board_frame.pack(pady=20, padx=20)
        
        # Create 3x3 grid of buttons
        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3
            
            button = ctk.CTkButton(
                self.board_frame,
                text="",
                width=100,
                height=100,
                font=ctk.CTkFont(size=32, weight="bold"),
                command=lambda pos=i: self._on_cell_click(pos)
            )
            button.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(button)
        
        # Reset button
        self.reset_button = ctk.CTkButton(
            self.root,
            text="New Game",
            font=ctk.CTkFont(size=16),
            command=self._reset_game
        )
        self.reset_button.pack(pady=20)
    
    def _on_cell_click(self, position: int):
        """Handle cell button click."""
        if self.game.make_move(position):
            # Update button text
            self.buttons[position].configure(
                text=self.game.board[position].value,
                state="disabled"
            )
            
            # Update status
            self._update_status()
    
    def _update_status(self):
        """Update the status label based on game state."""
        if self.game.state == GameState.PLAYING:
            self.status_label.configure(
                text=f"Player {self.game.current_player.value}'s turn"
            )
        elif self.game.state == GameState.DRAW:
            self.status_label.configure(text="It's a draw!")
        else:
            winner = self.game.get_winner()
            self.status_label.configure(text=f"Player {winner.value} wins!")
    
    def _reset_game(self):
        """Reset the game to initial state."""
        self.game.reset()
        
        # Clear all buttons
        for button in self.buttons:
            button.configure(text="", state="normal")
        
        # Reset status
        self._update_status()
    
    def run(self):
        """Start the GUI application."""
        # Set icon after everything is initialized (CustomTkinter workaround)
        if (hasattr(self, 'icon_path') and self.icon_path and
                self.icon_path.exists() and not self._ctk_headless):
            try:
                # Access the underlying Tkinter window
                self.root.after(10, lambda: self.root.iconbitmap(str(self.icon_path)))
            except:
                pass
        self.root.mainloop()


def main():
    """Entry point for the GUI application."""
    app = TicTacToeGUI()
    app.run()


if __name__ == "__main__":
    main()
