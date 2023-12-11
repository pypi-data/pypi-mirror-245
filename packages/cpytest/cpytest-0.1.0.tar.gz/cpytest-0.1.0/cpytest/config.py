"""CPYTEST configuration file reader (YAML)"""
from pathlib import Path
from textwrap import dedent
from typing import cast

import yaml

from cpytest import logger
from cpytest import path_util


log = logger.setup_logger("config")


class ConfigError(Exception):
    pass


class Config:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    def __init__(self, yaml_file: Path) -> None:
        assert yaml_file is not None
        if not yaml_file.is_file():
            raise FileNotFoundError(f"file not found: {yaml_file}")

        yaml_file = yaml_file.resolve()

        log.info(f"loading configuration from: {yaml_file}")

        with open(yaml_file, 'r', encoding='UTF-8') as file:
            cfg = yaml.safe_load(file)

        unit_cfg = self._get_cfg_group(cfg, 'unit')
        compiler_cfg = self._get_cfg_group(cfg, 'compiler')
        workspace_cfg = self._get_cfg_group(cfg, 'workspace')
        cffi_cfg = self._get_cfg_group(cfg, 'cffi', {})

        project_dir = yaml_file.parent
        try:
            project_dir = project_dir.relative_to(Path.cwd())
        except ValueError:
            # work with an absolute path, if the project_dir is not a sub-path of the current working directory
            pass

        self.project_dir = project_dir
        self.unit_name: str = self._get_cfg_str(unit_cfg, 'name')
        self.c_files: list[Path] = [Path(c_file) for c_file in self._get_cfg_list(unit_cfg, 'sources')]
        self.build_dir: Path = Path(self._get_cfg_str(workspace_cfg, 'build_dir'))
        self.py_stubs_dir = self.project_dir / self._get_cfg_str(workspace_cfg, 'stubs_dir', "stubs")

        try:
            path_util.py_module_path(self.project_dir, self.py_stubs_dir)
        except ValueError as exc:
            raise ConfigError(
                dedent(
                    f"""
                        Invalid 'stubs_dir' config path '{self.py_stubs_dir}' leads to invalid python module name.
                            A valid module name must start with a letter or underscore, and can only contain letters,
                            digits, and underscores.
                    """
                ).strip()
            ) from exc

        includes_cfg = self._get_cfg_group(compiler_cfg, 'includes', {})
        self.incl_rel_dir: Path = Path(self._get_cfg_str(includes_cfg, 'relative_to', ""))

        self.include_dirs: list[Path] = []
        self.include_dirs += [Path(inc) for inc in includes_cfg.get("paths", [])]
        if 'from_file' in includes_cfg:
            include_file = self.project_dir / includes_cfg["from_file"]
            self.include_dirs += self.read_include_file(include_file)

        self.gcc_args: list[str] = compiler_cfg.get("gcc_args", [])

        self.cffi_definitions: dict[str, list[str]] = {}
        self.cffi_definitions = self._get_cfg_group(cffi_cfg, "definitions", {})

        log.info(f"loaded configuration file from: {yaml_file}")
        log.debug(f"  project_dir:  {self.project_dir}")
        log.debug(f"  unit_name:    {self.unit_name}")
        log.debug(f"  c_files:      {self.c_files}")
        log.debug(f"  incl_rel_dir: {self.incl_rel_dir}")
        log.debug(f"  build_dir:    {self.build_dir}")
        log.debug(f"  stubs_dir:    {self.py_stubs_dir}")

    @classmethod
    def _get_cfg_group(cls, cfg: dict, key: str, default: dict | None = None) -> dict:
        if key not in cfg:
            if default is not None:
                return default
            raise ConfigError(f"missing mandatory configuration item: {key}")
        assert isinstance(cfg[key], dict)
        return cast(dict, cfg[key])

    @classmethod
    def _get_cfg_str(cls, cfg: dict, key: str, default: str | None = None) -> str:
        if key not in cfg:
            if default is not None:
                return default
            raise ConfigError(f"missing mandatory configuration item: {key}")
        assert isinstance(cfg[key], str)
        return cast(str, cfg[key])

    @classmethod
    def _get_cfg_list(cls, cfg: dict, key: str, default: list[str] | None = None) -> list[str]:
        if key not in cfg:
            if default is not None:
                return default
            raise ConfigError(f"missing mandatory configuration item: {key}")
        assert isinstance(cfg[key], list)
        return cast(list, cfg[key])

    @classmethod
    def read_include_file(cls, include_file: Path) -> list[Path]:
        assert include_file is not None
        assert isinstance(include_file, Path)

        log.debug(f"loading include_file: {include_file}")
        include_file = include_file.resolve()
        if not include_file.is_file():
            raise FileNotFoundError(f"file not found: {include_file}")

        include_dirs = set()
        with open(include_file, 'r', encoding='UTF-8') as file:
            for line in file.readlines():
                line = line.strip().strip('"').strip("'").lstrip('-I').strip()
                if len(line) > 0:
                    include_dirs.add(Path(line))
        return list(include_dirs)
