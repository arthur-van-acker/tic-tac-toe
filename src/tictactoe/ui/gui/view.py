"""Presentation layer utilities for the Tic Tac Toe GUI."""

from __future__ import annotations

from typing import Callable, List, Sequence

from tictactoe.domain.logic import GameSnapshot, GameState


class GameView:
    """Responsible for building and updating the widget tree."""

    def __init__(
        self,
        *,
        ctk_module,
        root,
        on_cell_click: Callable[[int], None],
        on_reset: Callable[[], None],
    ) -> None:
        self.ctk = ctk_module
        self.root = root
        self._on_cell_click = on_cell_click
        self._on_reset = on_reset

        self.title_label = None
        self.status_label = None
        self.board_frame = None
        self.reset_button = None
        self.buttons: List[object] = []

    def build(self) -> None:
        """Construct all widgets for the application."""

        font_bold_title = self.ctk.CTkFont(size=32, weight="bold")
        font_status = self.ctk.CTkFont(size=20)
        font_button = self.ctk.CTkFont(size=32, weight="bold")
        font_reset = self.ctk.CTkFont(size=16)

        self.title_label = self.ctk.CTkLabel(
            self.root,
            text="Tic Tac Toe",
            font=font_bold_title,
        )
        self.title_label.pack(pady=20)

        self.status_label = self.ctk.CTkLabel(self.root, text="", font=font_status)
        self.status_label.pack(pady=10)

        self.board_frame = self.ctk.CTkFrame(self.root)
        self.board_frame.pack(pady=20, padx=20)

        self._build_board(font_button)
        self._build_reset_button(font_reset)

    def _build_board(self, font_button) -> None:
        """Create the 3x3 grid of buttons."""

        self.buttons = []
        for position in range(9):
            button = self.ctk.CTkButton(
                self.board_frame,
                text="",
                width=100,
                height=100,
                font=font_button,
                command=lambda pos=position: self._on_cell_click(pos),
            )
            button.grid(row=position // 3, column=position % 3, padx=5, pady=5)
            self.buttons.append(button)

    def _build_reset_button(self, font_reset) -> None:
        self.reset_button = self.ctk.CTkButton(
            self.root,
            text="New Game",
            font=font_reset,
            command=self._on_reset,
        )
        self.reset_button.pack(pady=20)

    def render(self, snapshot: GameSnapshot) -> None:
        """Update the widget state to reflect the game snapshot."""

        self._render_board(snapshot.board)
        self._render_status(snapshot)

    def _render_board(self, board: Sequence) -> None:
        for position, button in enumerate(self.buttons):
            cell = board[position]
            if cell is None:
                button.configure(text="", state="normal")
            else:
                button.configure(text=cell.value, state="disabled")

    def _render_status(self, snapshot: GameSnapshot) -> None:
        if snapshot.state == GameState.PLAYING:
            self.status_label.configure(text=f"Player {snapshot.current_player.value}'s turn")
        elif snapshot.state == GameState.DRAW:
            self.status_label.configure(text="It's a draw!")
        else:
            winner = snapshot.winner.value if snapshot.winner else "Unknown"
            self.status_label.configure(text=f"Player {winner} wins!")
