"""CFFI builder to compile the generated CFFI interface library."""

import os
from pathlib import Path

from cffi import FFI

from cpytest import logger
from cpytest.config import Config


log = logger.setup_logger("cffi")


class CpyFfiBuilder:  # pylint: disable=too-few-public-methods
    def __init__(self, config: Config) -> None:
        self._config = config

    def compile(  # pylint: disable=too-many-locals
        self,
        cffi_interface_c_file: Path,
        cffi_header_file: Path,
    ) -> None:
        assert isinstance(cffi_interface_c_file, Path)
        assert isinstance(cffi_header_file, Path)
        assert cffi_interface_c_file.is_file(), f"file not found: {cffi_interface_c_file}"
        assert cffi_header_file.is_file(), f"file not found: {cffi_header_file}"

        workdir = self._config.project_dir
        incl_rel_dir = workdir / self._config.incl_rel_dir
        build_dir = workdir / self._config.build_dir
        source_files = self._config.c_files

        workdir_rel = os.path.relpath(workdir, start=build_dir)
        source_dir_rel = os.path.relpath(incl_rel_dir, start=build_dir)

        relative_source_files = [os.path.normpath(workdir_rel / source_file) for source_file in source_files]

        relative_include_dirs = [
            os.path.normpath(source_dir_rel / include_dir) for include_dir in (self._config.include_dirs or [])
        ]

        ffibuilder = FFI()

        with open(cffi_header_file, "r", encoding='UTF-8') as file:
            ffibuilder.cdef(file.read())

        coverage_args = [
            "-fprofile-arcs",
            "-ftest-coverage",
        ]
        warnings_args = [
            "-Wno-array-parameter",  # cffi will convert fixed size arrays to pointers, which causes warnings
        ]
        config_args = self._config.gcc_args

        link_args = [
            "-lgcov",
        ]

        compile_args = coverage_args + warnings_args + config_args

        log.info(f"build_dir:      {build_dir}")
        log.info(f"cffi-interface: {cffi_interface_c_file}")
        log.info(f"cffi-header:    {cffi_header_file}")
        log.debug(f"compile_args:   {compile_args}")
        log.debug(f"link_args:      {link_args}")

        with open(cffi_interface_c_file, "r", encoding='UTF-8') as file:
            cffi_c_code = file.read()

        ffibuilder.set_source(
            self._config.unit_name,
            source=cffi_c_code,
            sources=relative_source_files,
            include_dirs=relative_include_dirs,
            libraries=[],
            extra_compile_args=compile_args,
            extra_link_args=link_args,
        )

        so_file = ffibuilder.compile(verbose=True, tmpdir=build_dir)

        log.info(f"generated interface library: {so_file}")
