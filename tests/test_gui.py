"""Lightweight GUI smoke tests for TicTacToeGUI."""

from __future__ import annotations

import os
import platform

import pytest

from tkinter import TclError

from tictactoe.ui.gui.main import TicTacToeGUI


NEEDS_DISPLAY = platform.system() != "Windows" and not os.environ.get("DISPLAY")


def _skip_if_no_display() -> None:
    if NEEDS_DISPLAY:
        pytest.skip("GUI tests require a display")


def _create_app_or_skip() -> TicTacToeGUI:
    _skip_if_no_display()
    try:
        return TicTacToeGUI()
    except TclError as exc:
        if "tcl_findLibrary" in str(exc):
            pytest.skip("Tk runtime is unavailable in this environment")
        raise


@pytest.mark.gui
def test_gui_initializes_widgets():
    app = _create_app_or_skip()
    try:
        assert len(app.buttons) == 9
        assert "Player X" in app.status_label.cget("text")
        assert app.reset_button.cget("text") == "New Game"
    finally:
        app.root.destroy()


@pytest.mark.gui
def test_gui_click_updates_button_and_status():
    app = _create_app_or_skip()
    try:
        app._on_cell_click(0)
        assert app.buttons[0].cget("text") == "X"
        assert app.buttons[0].cget("state") == "disabled"
        assert "Player O" in app.status_label.cget("text")
    finally:
        app.root.destroy()
