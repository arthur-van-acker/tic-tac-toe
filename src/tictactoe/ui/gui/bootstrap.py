"""Bootstrap helpers for the CustomTkinter GUI layer."""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from tkinter import TclError
from types import ModuleType
from typing import Optional, Tuple


def _import_headless_module() -> ModuleType:
    from tictactoe.ui.gui import headless as headless_ctk

    return headless_ctk


@dataclass(frozen=True)
class CtkEnvironment:
    """Represents the currently loaded CustomTkinter module and mode."""

    module: ModuleType
    headless: bool


def load_customtkinter(force_headless: bool = False) -> CtkEnvironment:
    """Load CustomTkinter or fall back to the headless shim."""

    if force_headless or os.environ.get("TICTACTOE_HEADLESS") == "1":
        return CtkEnvironment(module=_import_headless_module(), headless=True)

    try:
        import customtkinter as real_ctk

        return CtkEnvironment(module=real_ctk, headless=False)
    except Exception:
        return CtkEnvironment(module=_import_headless_module(), headless=True)


def configure_windows_app_model(app_id: str = "TicTacToe.Game.v0.1.0") -> None:
    """Ensure Windows shows a dedicated taskbar icon for the app."""

    if platform.system() != "Windows":
        return

    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except (AttributeError, OSError):
        pass


def create_root(env: CtkEnvironment) -> Tuple[ModuleType, object, CtkEnvironment]:
    """Create the CTk root window, retrying in headless mode if needed."""

    try:
        return env.module, env.module.CTk(), env
    except TclError:
        if env.headless:
            raise
        fallback_env = load_customtkinter(force_headless=True)
        return fallback_env.module, fallback_env.module.CTk(), fallback_env


def locate_icon_file() -> Optional[Path]:
    """Find the favicon in either the source tree or installed package."""

    candidates = [
        Path(__file__).parent.parent.parent / "assets" / "favicon.ico",
        Path(sys.prefix) / "Lib" / "site-packages" / "tictactoe" / "assets" / "favicon.ico",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def apply_window_icon(root: object, icon_path: Optional[Path], *, headless: bool) -> None:
    """Set the window icon when running with a real Tk backend."""

    if headless or icon_path is None:
        if icon_path is None:
            print("Warning: Icon file not found")
        return

    try:
        root.iconbitmap(default=str(icon_path))
    except TclError as exc:
        print(f"Warning: Could not set icon: {exc}")


def schedule_icon_refresh(root: object, icon_path: Optional[Path], *, headless: bool) -> None:
    """Schedule a delayed icon update to work around CustomTkinter quirks."""

    if headless or icon_path is None:
        return

    try:
        root.after(10, lambda: root.iconbitmap(str(icon_path)))
    except (TclError, AttributeError):
        pass
