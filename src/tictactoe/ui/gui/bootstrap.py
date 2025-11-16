"""Bootstrap helpers for the CustomTkinter GUI layer."""

from __future__ import annotations

import os
import platform
import shutil
import sys
import tempfile
from dataclasses import dataclass
from importlib import resources
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


_ICON_CACHE: Optional[Path] = None


def locate_icon_file() -> Optional[Path]:
    """Resolve the favicon path from source or installed package data."""

    global _ICON_CACHE

    if _ICON_CACHE and _ICON_CACHE.exists():
        return _ICON_CACHE

    source_candidate = Path(__file__).resolve().parent.parent.parent / "assets" / "favicon.ico"
    if source_candidate.exists():
        _ICON_CACHE = source_candidate
        return source_candidate

    package_candidate = _locate_package_icon()
    if package_candidate is not None:
        _ICON_CACHE = package_candidate
        return package_candidate

    return None


def _locate_package_icon() -> Optional[Path]:
    """Locate the icon via importlib.resources for installed packages."""

    try:
        icon_resource = resources.files("tictactoe") / "assets" / "favicon.ico"
    except ModuleNotFoundError:
        return None

    try:
        icon_path = Path(icon_resource)
        if icon_path.exists():
            return icon_path
    except TypeError:
        pass

    try:
        with resources.as_file(icon_resource) as extracted_path:
            extracted = Path(extracted_path)
            if not extracted.exists():
                return None
            temp_dir = Path(tempfile.gettempdir()) / "tictactoe"
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_path = temp_dir / "favicon.ico"
            shutil.copyfile(extracted, temp_path)
            return temp_path
    except FileNotFoundError:
        return None

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
