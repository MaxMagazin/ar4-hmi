from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_robot_kinematics_shim():
	package_dir = Path(__file__).resolve().parent
	shim_path = package_dir / "robot_kinematics.py"
	spec = importlib.util.spec_from_file_location(
		"ARrobots._robot_kinematics_shim",
		shim_path,
	)
	if spec is None or spec.loader is None:
		raise ImportError(f"Could not load robot kinematics shim from {shim_path}")

	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	sys.modules[f"{__name__}.robot_kinematics"] = module
	return module


robot_kinematics = _load_robot_kinematics_shim()
