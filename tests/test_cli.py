"""Tests for the CLI entry point."""

from importlib import import_module, reload


def test_cli_main_invokes_gui(monkeypatch):
    gui_module = import_module("tictactoe.ui.gui.main")
    called = {"count": 0}

    def fake_main():
        called["count"] += 1

    monkeypatch.setattr(gui_module, "main", fake_main)

    cli_module = reload(import_module("tictactoe.__main__"))
    cli_module.main()

    assert called["count"] == 1
