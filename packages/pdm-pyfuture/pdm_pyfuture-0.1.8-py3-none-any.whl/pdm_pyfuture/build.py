from __future__ import annotations

import sys
from pathlib import Path

from pdm.backend.base import Context
from pyfuture.utils import transfer_file


class PyFutureBuildHook:
    def hook_config(self, context: Context):
        return context.config.data.get("tool", {}).get("pdm", {}).get("build", {}).get("hooks", {}).get("pyfuture", {})

    def pdm_build_hook_enabled(self, context: Context):
        # TODO: support editable
        # hook_config = self.hook_config(context)
        # enable_editable = hook_config.get("enable_editable", True)
        # return context.target == "wheel" or (not enable_editable and context.target == "editable")
        return context.target == "wheel"

    def pdm_build_initialize(self, context: Context) -> None:
        context.config.build_config["is-purelib"] = True
        context.builder.config_settings["--python-tag"] = f"py{sys.version_info.major}{sys.version_info.minor}"

    def pdm_build_update_files(self, context: Context, files: dict[str, Path]) -> None:
        build_dir = context.ensure_build_dir()
        package_dir = Path(context.config.build_config.package_dir)
        includes = context.config.build_config.includes
        for include in includes:
            src_path = package_dir / include
            tgt_path = build_dir / include
            for src_file in src_path.glob("**/*.py"):
                tgt_file = tgt_path / src_file.relative_to(src_path)
                files[f"{tgt_file.relative_to(build_dir)}"] = tgt_file
                # TODO: support config target
                transfer_file(src_file, tgt_file, target=sys.version_info[:2])
