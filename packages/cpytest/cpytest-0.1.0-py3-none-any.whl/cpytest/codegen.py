"""Code generator for CFFI interface files."""

import os
from pathlib import Path
import subprocess
import sys
from textwrap import dedent

from pycparser.plyparser import Coord

from cpytest.config import Config
from cpytest.parse import ParserResults
from cpytest import path_util
from cpytest.type import CpyFunc, CpyType
from cpytest import logger


log = logger.setup_logger("codegen")


class CodeGenError(Exception):
    pass


class CodeGenerator:
    def __init__(self, config: Config, parse_results: ParserResults, cpy_prefix: str = "__cpy__") -> None:
        self._config = config
        self._parse_results = parse_results
        self._cpy_prefix = cpy_prefix

    @classmethod
    def _c_banner(cls, text: str, width: int = 80) -> str:
        width = min(width - 4, 2)
        return f"/*{'*' * width}*/\n// {text}\n/*{'*' * width}*/\n"

    def gen_cpy_source_file(self, out_file: Path) -> None:
        with open(out_file, "w", encoding='utf-8') as f:
            f.write(
                dedent(
                    f"""
                        /**
                        * CFFI external interface for test unit: {self._config.unit_name}
                        * @author {Path(__file__).name}
                        */
                    """
                ).lstrip('\n')
            )
            f.write('\n')

            f.write(self._c_banner("Includes (types and functions)"))
            for header_file in self._parse_results.include_files:
                f.write(f'#include "{Path(header_file).name}"\n')
            f.write('\n')

            # includes from defines (WIP)
            f.write(self._c_banner("Includes from defines (WIP)"))
            for header in self._config.cffi_definitions.keys() - self._parse_results.include_files:
                f.write(f"#include \"{header}\"\n")
            f.write('\n')

            for source_file, cpy_funcs in self._parse_results.ext_cpy_funcs.items():
                f.write(
                    self._c_banner(
                        f"External dependencies declarations: {self.relative_project_path(out_file, source_file)}"
                    )
                )
                for cpy_func in cpy_funcs:
                    f.write(
                        dedent(
                            f"""
                                {cpy_func.c_signature_str(name_prefix=self._cpy_prefix, storage='static')};
                                {cpy_func.c_signature_str(storage='extern')}
                                {{
                                    {cpy_func.c_call_str(name_prefix=self._cpy_prefix)};
                                }}
                            """
                        ).lstrip('\n')
                    )
                    f.write('\n')
        log.info(f"Generated {out_file}")

    def gen_cpy_header_file(self, out_file: Path) -> None:
        with open(out_file, "w", encoding='utf-8') as f:
            f.write(
                dedent(
                    f"""
                        /**
                        * CFFI header for test unit: {self._config.unit_name}
                        * @author {Path(__file__).name}
                        */
                    """
                ).lstrip('\n')
            )
            f.write('\n')

            # static definitions (WIP)
            f.write(self._c_banner("Static definitions (WIP)"))
            for header, defines in self._config.cffi_definitions.items():
                f.write(f"// defined in '{header}'\n")
                for define in defines:
                    f.write(f"#define {define} ...\n")
            f.write('\n')

            # create type definitions for everything found externally
            f.write(self._c_banner("Type definitions"))
            for type_def in self._parse_results.all_cpy_types:
                relative_coord = self.relative_project_coord(out_file, type_def.typedef.coord, full=True)
                f.write(f"// included from: {relative_coord}\n")
                f.write(f"{type_def.to_string()};\n")
                f.write('\n')

            # create declarations for local public functions
            for source_file, cpy_funcs in self._parse_results.local_cpy_funcs.items():
                f.write(
                    self._c_banner(
                        f"Local declarations for source file: {self.relative_project_path(out_file, source_file)}"
                    )
                )
                for cpy_func in cpy_funcs:
                    f.write(f"{cpy_func.c_signature_str()};\n")
                f.write('\n')

            # create python stub definitions for external functions
            f.write(self._c_banner("Python stubs for external dependencies"))
            for source_file, cpy_funcs in self._parse_results.ext_cpy_funcs.items():
                for cpy_func in cpy_funcs:
                    func_decl_str = cpy_func.c_signature_str(name_prefix=self._cpy_prefix, storage='extern "Python"')
                    f.write(f"{func_decl_str};\n")

        log.info(f"Generated {out_file}")

    def gen_cpy_py_stub_files(self, stubs_dir: Path) -> list[Path]:
        py_module_path = path_util.py_module_path(
            self._config.project_dir, self._config.build_dir / self._config.unit_name
        )
        stub_files = []

        for source_file, ext_cpy_funcs in self._parse_results.ext_cpy_funcs.items():
            py_stub_file = stubs_dir / f"{source_file.stem}.py"
            log.info(f"Generating python stub: {py_stub_file}")
            used_cpy_types = self._parse_results.used_cpy_types.get(source_file, [])
            self.gen_cpy_py_stub_file(py_stub_file, ext_cpy_funcs, used_cpy_types, py_module_path)
            stub_files.append(py_stub_file)

        return stub_files

    def gen_cpy_py_stub_file(  # pylint: disable=too-many-locals
        self, out_file: Path, ext_cpy_funcs: list[CpyFunc], used_cpy_types: list[CpyType], py_module_path: str
    ) -> None:
        with open(out_file, "w", encoding='utf-8') as f:
            f.write(
                dedent(
                    f"""
                        from typing import Any, NewType

                        from _cffi_backend import __CDataOwn as CData

                        from {py_module_path} import ffi, lib
                    """
                )
            )

            if used_cpy_types:
                f.write('\n')
                f.write('\n')

            for cpy_type in used_cpy_types:
                type_name = cpy_type.typedef.name
                aliased_str = None
                if cpy_type.is_enum():
                    aliased_str = "int"
                elif cpy_type.is_struct():
                    aliased_str = "Any"

                if aliased_str is not None:
                    relative_coord = self.relative_project_coord(out_file, cpy_type.typedef.coord)
                    f.write(
                        dedent(
                            f"""
                                # type alias: {type_name} ({relative_coord})
                                {type_name} = NewType('{type_name}', {aliased_str})
                            """
                        ).lstrip('\n')
                    )

            # create python stub definitions for external functions
            for cpy_func in ext_cpy_funcs:
                f.write('\n')
                func_def_ext_str = cpy_func.py_signature_str(name_prefix=self._cpy_prefix)
                func_call_str = cpy_func.py_call_return_str()
                stub_def = cpy_func.py_signature_str()
                stub_default_return_str = cpy_func.py_default_return_str()
                stub_return_str = f"return {stub_default_return_str}" if stub_default_return_str is not None else "pass"
                relative_coord = self.relative_project_coord(out_file, cpy_func.decl.coord)
                f.write(
                    dedent(
                        f"""
                            @ffi.def_extern()
                            {func_def_ext_str}:
                                \"\"\"CFFI callback for external function `{cpy_func.decl.name}()`.\"\"\"
                                {func_call_str}

                            {stub_def}:
                                \"\"\"Mockable stub for external function `{cpy_func.decl.name}()`.

                                C function signature:
                                ```
                                    {cpy_func.c_signature_str()};
                                ```
                                (from: {relative_coord})
                                \"\"\"
                                {stub_return_str}
                        """
                    )
                )

    def gen_pytest_template(self, pytest_file: Path) -> None:
        stubs_py_path = path_util.py_module_path(self._config.project_dir, self._config.py_stubs_dir)
        ext_funcs = self._parse_results.ext_cpy_funcs
        local_func_defs = self._parse_results.local_cpy_func_defs

        with pytest_file.open('w', encoding='utf-8') as f:
            f.write(
                dedent(
                    f"""
                        import pytest
                        from unittest.mock import patch, MagicMock

                        from build.{self._config.unit_name} import lib, ffi

                        from _cffi_backend import __CDataOwn as CData

                        # important to import the stubs to register the external functions to cffi
                    """
                )
            )

            for source_file, _ in ext_funcs.items():
                f.write(f"import {stubs_py_path}.{source_file.stem}\n")
            f.write('\n')
            f.write('\n')

            for source_file, func_defs in local_func_defs.items():
                for func in func_defs:
                    patch_args: list[str] = []
                    called_decls = func.get_called_func_decls()
                    for cpy_func in called_decls:
                        ext_path = Path(cpy_func.decl.coord.file)
                        patch_args.append(f"{cpy_func.decl.name}: MagicMock")
                        f.write(f"@patch('{stubs_py_path}.{ext_path.stem}.{cpy_func.decl.name}')\n")

                    patch_args.reverse()
                    f.write(f"def test_{func.decl.name}({', '.join(patch_args)}) -> None:\n")

                    for cpy_func in called_decls:
                        default_value_str = cpy_func.py_default_return_str()
                        if default_value_str is not None:
                            f.write(f"    {cpy_func.decl.name}.return_value = {default_value_str}\n")

                    f.write(f"    lib.{func.py_call_default_str()}\n")
                    f.write('\n')

    def relative_project_path(self, base: Path, file: Path) -> Path:
        """Convert a file path, which is relative to a base path, to a path relative to the project dir.

        Consider `file` is relative to `base`, i.e. `base/xxx/file`.
        And `base` is relative to the project dir: `project_dir/yyy/base`.
        Then the relative path is: `project_dir/yyy/base/xxx/file`.

        The output path is normalized, i.e. all `.` and `..` are resolved.

        Note that the `base` path can be a file, in which case the relative path is relative to the parent directory.
        Note that technically `file` can also be a directory.
        """
        assert isinstance(base, Path)
        assert isinstance(file, Path)

        base_dir = base if base.is_dir() else base.parent
        workdir_rel = os.path.relpath(self._config.project_dir, start=base_dir)
        return Path(os.path.normpath(os.path.join(workdir_rel, file)))

    def relative_project_coord(self, base: Path, coord: Coord, full: bool = False) -> str:
        """Return a string representation of a Coord relative to a base path."""
        assert isinstance(base, Path)
        assert isinstance(coord, Coord)

        rel_path = self.relative_project_path(base, Path(coord.file))
        return str(rel_path) if not full else f"{rel_path}:{coord.line}:{coord.column}"

    def format_py_files(self, py_files: list[Path]) -> None:
        for py_file in py_files:
            try:
                subprocess.run([sys.executable, "-m", "black", py_file, "--quiet"], check=True, capture_output=True)
            except subprocess.CalledProcessError as exc:
                raise CodeGenError(f"Error formatting {py_file}: {exc.stderr.decode()}") from exc

            log.debug(f"formatted (black): {py_file}")
