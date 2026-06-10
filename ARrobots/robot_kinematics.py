"""Compatibility shim for loading the compiled robot_kinematics extension.

The native extension is built as top-level module "robot_kinematics" by
ARrobots/src/CMakeLists.txt, while app code imports it as
"ARrobots.robot_kinematics".
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path


def _candidate_dirs() -> list[Path]:
    pkg_dir = Path(__file__).resolve().parent
    repo_dir = pkg_dir.parent
    return [
        repo_dir,
        repo_dir / "ARrobots" / "src" / "build",
        repo_dir / "ARrobots" / "src" / "build" / "Release",
    ]


def _import_native_module():
    for directory in _candidate_dirs():
        path_text = str(directory)
        if directory.exists() and path_text not in sys.path:
            sys.path.insert(0, path_text)

    try:
        module = importlib.import_module("robot_kinematics")
        if Path(getattr(module, "__file__", "")).resolve() == Path(__file__).resolve():
            raise ModuleNotFoundError
        return module
    except ModuleNotFoundError:
        pass

    for directory in _candidate_dirs():
        if not directory.exists():
            continue
        for ext_path in sorted(directory.glob("robot_kinematics*.so")):
            spec = importlib.util.spec_from_file_location("robot_kinematics", ext_path)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

    raise ModuleNotFoundError(
        "Could not load native module 'robot_kinematics'. "
        "Build it from ARrobots/src with: ./build_kinematics.sh"
    )


_native = _import_native_module()

__all__ = [name for name in dir(_native) if not name.startswith("_")]

for _name in __all__:
    globals()[_name] = getattr(_native, _name)
