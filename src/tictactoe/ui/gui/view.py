"""Presentation layer utilities for the Tic Tac Toe GUI."""

from __future__ import annotations

from typing import Callable, Dict, List, Sequence

from tictactoe.config import FontSpec, GameViewConfig
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
        view_config: GameViewConfig | None = None,
    ) -> None:
        self.ctk = ctk_module
        self.root = root
        self._on_cell_click = on_cell_click
        self._on_reset = on_reset
        self.config = view_config or GameViewConfig()

        self.title_label = None
        self.status_label = None
        self.board_frame = None
        self.reset_button = None
        self.buttons: List[object] = []

    def build(self) -> None:
        """Construct all widgets for the application."""

        fonts = self._build_fonts()

        self.title_label = self.ctk.CTkLabel(
            self.root,
            text=self.config.text.title,
            font=fonts["title"],
            **self._text_color_kwargs(self.config.colors.title_text),
        )
        self.title_label.pack(pady=self.config.layout.title_padding)

        self.status_label = self.ctk.CTkLabel(
            self.root,
            text="",
            font=fonts["status"],
            **self._text_color_kwargs(self.config.colors.status_text),
        )
        self.status_label.pack(pady=self.config.layout.status_padding)

        board_frame_kwargs = self._frame_color_kwargs()
        self.board_frame = self.ctk.CTkFrame(self.root, **board_frame_kwargs)
        pady, padx = self.config.layout.board_padding
        self.board_frame.pack(pady=pady, padx=padx)

        self._build_board(fonts["cell"])
        self._build_reset_button(fonts["reset"])

    def _build_board(self, font_button) -> None:
        """Create the 3x3 grid of buttons."""

        self.buttons = []
        for position in range(9):
            button_kwargs = self._cell_button_color_kwargs()
            button = self.ctk.CTkButton(
                self.board_frame,
                text="",
                width=self.config.layout.cell_size[0],
                height=self.config.layout.cell_size[1],
                font=font_button,
                command=lambda pos=position: self._on_cell_click(pos),
                **button_kwargs,
            )
            button.grid(
                row=position // 3,
                column=position % 3,
                padx=self.config.layout.cell_spacing,
                pady=self.config.layout.cell_spacing,
            )
            self.buttons.append(button)

    def _build_reset_button(self, font_reset) -> None:
        reset_kwargs = self._reset_button_color_kwargs()
        self.reset_button = self.ctk.CTkButton(
            self.root,
            text=self.config.text.reset_button,
            font=font_reset,
            command=self._on_reset,
            **reset_kwargs,
        )
        self.reset_button.pack(pady=self.config.layout.reset_padding)

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
        text = self._status_message(snapshot)
        self.status_label.configure(text=text)

    def _build_fonts(self) -> Dict[str, object]:
        """Instantiate the CustomTkinter fonts from the config."""

        return {
            "title": self._create_font(self.config.fonts.title),
            "status": self._create_font(self.config.fonts.status),
            "cell": self._create_font(self.config.fonts.cell),
            "reset": self._create_font(self.config.fonts.reset),
        }

    def _create_font(self, spec: FontSpec):
        kwargs = {"size": spec.size}
        if spec.weight:
            kwargs["weight"] = spec.weight
        return self.ctk.CTkFont(**kwargs)

    def _text_color_kwargs(self, color: str | None) -> Dict[str, str]:
        return {"text_color": color} if color else {}

    def _cell_button_color_kwargs(self) -> Dict[str, str]:
        colors = self.config.colors
        kwargs: Dict[str, str] = {}
        if colors.cell_text:
            kwargs["text_color"] = colors.cell_text
        if colors.cell_fg:
            kwargs["fg_color"] = colors.cell_fg
        if colors.cell_hover:
            kwargs["hover_color"] = colors.cell_hover
        return kwargs

    def _reset_button_color_kwargs(self) -> Dict[str, str]:
        colors = self.config.colors
        kwargs: Dict[str, str] = {}
        if colors.reset_fg:
            kwargs["fg_color"] = colors.reset_fg
        return kwargs

    def _frame_color_kwargs(self) -> Dict[str, str]:
        if not self.config.colors.board_background:
            return {}
        return {"fg_color": self.config.colors.board_background}

    def _status_message(self, snapshot: GameSnapshot) -> str:
        if snapshot.state == GameState.PLAYING:
            player = snapshot.current_player.value if snapshot.current_player else "?"
            return self.config.text.turn_message_template.format(player=player)
        if snapshot.state == GameState.DRAW:
            return self.config.text.draw_message
        winner = snapshot.winner.value if snapshot.winner else "Unknown"
        return self.config.text.win_message_template.format(winner=winner)
