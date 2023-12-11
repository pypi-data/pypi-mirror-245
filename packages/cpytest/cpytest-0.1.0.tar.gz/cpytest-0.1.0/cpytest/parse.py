"""Parser module for encapsulating the pycparser parser."""

from pathlib import Path
import re
from typing import Set

import pycparser
from pycparser import c_ast
from pycparser.plyparser import Coord
from pycparserext import ext_c_parser as c_ext

from cpytest.config import Config
from cpytest.type import CpyFunc, CpyFuncDef, CpyType, Typeref
from cpytest.preproc import Preproc
from cpytest import logger


log = logger.setup_logger("parse")


class CpyVisitor(c_ast.NodeVisitor):  # type: ignore[misc]  # pylint: disable=too-many-instance-attributes
    def __init__(self, system_headers: list[Path]) -> None:
        self._system_headers = system_headers
        self._func_decls: list[c_ast.Decl] = []
        self._func_defs: list[c_ast.FuncDef] = []
        self._func_calls: list[c_ast.FuncCall] = []
        self._typedefs: list[Typeref] = []
        self._pack_stack: list[int | None] = [None]

    def _add_typedef(self, typedef: c_ast.Typedef) -> None:
        """Add a typedef to the list of typedefs.

        This function first searches for a referenced typedef, i.e. another already found typedef, which has the same
        typedefed declaration. The same typedefed declaration means that the typedefed declaration has the same
        coordinates. If such a typedef is found, the new typedef is added with a reference to the found typedef.
        """
        typedefed_coord = Typeref.get_typedefed_decl(typedef).coord
        reference_typedef = None

        for existing in self._typedefs:
            if existing.typedef.name == typedef.name and str(typedef.coord) == str(existing.typedef.coord):
                return

        for other_typedef in self._typedefs:
            other_coord = Typeref.get_typedefed_decl(other_typedef.typedef).coord
            if typedefed_coord == other_coord:
                reference_typedef = other_typedef.typedef
                break
        self._typedefs.append(Typeref(typedef, reference_typedef, self._pack_stack[-1]))

    def _add_func_decl(self, func_decl: c_ast.Decl) -> None:
        assert isinstance(func_decl, c_ast.Decl)
        assert isinstance(func_decl.type, c_ext.FuncDeclExt)
        for existing in self._func_decls:
            if existing.name == func_decl.name:
                return
        self._func_decls.append(func_decl)

    def visit_Pragma(self, node: c_ast.Pragma) -> None:  # pylint: disable=invalid-name
        # https://regex101.com/r/p9K9eg/1
        pattern = re.compile(r"pack\(\s*(push|pop)(\s*,\s*(\d+))?\s*\)")
        match = pattern.match(node.string)
        if match:
            if match.group(1) == "push":
                self._pack_stack.append(int(match.group(3) or 0))
            elif match.group(1) == "pop":
                self._pack_stack.pop()
            else:
                raise NotImplementedError(f"match.group(1): {match.group(1)} {node.coord}")
        super().generic_visit(node)

    def _is_system_header(self, coord: Coord) -> bool:
        return Path(coord.file) in self._system_headers

    def visit_Typedef(self, node: c_ast.Typedef) -> None:  # pylint: disable=invalid-name
        if not self._is_system_header(node.coord):
            self._add_typedef(node)
        super().generic_visit(node)

    def visit_Decl(self, node: c_ast.Decl) -> None:  # pylint: disable=invalid-name
        if isinstance(node.type, c_ext.FuncDeclExt):
            if 'static' not in node.storage:
                self._add_func_decl(node)
        super().generic_visit(node)

    def visit_FuncDef(self, node: c_ast.FuncDef) -> None:  # pylint: disable=invalid-name
        if isinstance(node.decl.type, c_ext.FuncDeclExt):
            self._func_defs.append(node)
        super().generic_visit(node)

    def visit_FuncCall(self, node: c_ast.FuncCall) -> None:  # pylint: disable=invalid-name
        if isinstance(node.name, c_ast.ID):
            self._func_calls.append(node)
        super().generic_visit(node)

    @classmethod
    def _is_local_coord(cls, coord: Coord, local_c_files: list[Path]) -> bool:
        return any(Path(coord.file) == c_file for c_file in local_c_files)

    def _find_external_function_decl(self, name: str, local_c_files: list[Path]) -> c_ast.Decl | None:
        """Return the first external declaration of a function with name 'name', if there is no local declaration.

        If there is a local declaration, return None.
        """
        ext_decl = None
        for func_decl in self._func_decls:
            if func_decl.name == name:
                if self._is_local_coord(func_decl.coord, local_c_files):
                    return None
                if ext_decl is None and not self._is_system_header(func_decl.coord):
                    ext_decl = func_decl
                    # note: don't break or return here - we might still find alocal declaration
        return ext_decl

    def find_definition_for_func_name(self, name: str) -> c_ast.FuncDef | None:
        for func_def in self._func_defs:
            if func_def.decl.name == name:
                return func_def
        return None

    def find_declaration_for_func_name(self, name: str) -> c_ast.Decl | None:
        for func_decl in self._func_decls:
            if func_decl.name == name and not self._is_system_header(func_decl.coord):
                return func_decl
        return None

    def get_external_called_decl(self, local_c_files: list[Path]) -> list[c_ast.Decl]:
        """Return the declarations of external functions that are called in the local file."""

        def _add_decl(decls: list[c_ast.Decl], decl: c_ast.Decl) -> None:
            for existing in decls:
                if existing.name == decl.name:
                    return
            decls.append(decl)

        decls: list[c_ast.Decl] = []
        for func_call in self._func_calls:
            if self._is_local_coord(func_call.coord, local_c_files):
                decl = self._find_external_function_decl(func_call.name.name, local_c_files)
                if decl is not None:
                    func_def = self.find_definition_for_func_name(decl.name)
                    if func_def is None:
                        _add_decl(decls, decl)
        return decls

    def get_local_func_decls(self, local_c_files: list[Path]) -> list[c_ast.Decl]:
        """Return all declarations of functions that are defined in the local file."""
        return [
            func_def.decl
            for func_def in self._func_defs
            if 'static' not in func_def.decl.storage and self._is_local_coord(func_def.coord, local_c_files)
        ]

    def get_local_func_defs(self) -> list[c_ast.FuncDef]:
        return [func_def for func_def in self._func_defs if 'static' not in func_def.decl.storage]

    def get_all_typedefs(self) -> list[Typeref]:
        return self._typedefs

    def get_include_files(self, local_c_files: list[Path]) -> list[str]:
        include_files: Set[str] = set()

        # add includes from non-local typedefs
        for typedef in self._typedefs:
            if typedef.typedef.coord is not None and not self._is_local_coord(typedef.typedef.coord, local_c_files):
                include_files.add(Path(typedef.typedef.coord.file).name)

        # add includes from locally defined, externally declared functions
        for func_def in self._func_defs:
            if self._is_local_coord(func_def.coord, local_c_files):
                # only when defined locally
                func_decl = self.find_declaration_for_func_name(func_def.decl.name)
                if func_decl is not None:
                    if not self._is_local_coord(func_decl.coord, local_c_files):
                        # only when declared externally
                        include_files.add(Path(func_decl.coord.file).name)

        return list(include_files)


class Parser:
    def __init__(self, config: Config) -> None:
        self._config = config

    def parse(self) -> 'ParserResults':
        c_files = self._config.c_files

        system_headers: set[Path] = set()

        for c_file in c_files:
            i_file = self._config.build_dir / f"{c_file.stem}.i"
            p_file = self._config.build_dir / f"{c_file.stem}.p"

            workdir = self._config.project_dir
            incl_rel_dir = self._config.incl_rel_dir

            preproc = Preproc(workdir=workdir)

            log.info(f"Preprocessing:   {c_file}")
            log.debug(f"  workdir:      {workdir}")
            log.debug(f"  c_file:       {c_file}")
            log.debug(f"  i_file:       {workdir / i_file}")
            log.debug(f"  pp_file:      {workdir / p_file}")
            log.debug(f"  incl_rel_dir: {incl_rel_dir}")
            preproc.preprocess(
                c_file,
                outfile=i_file,
                incl_rel_dir=incl_rel_dir,
                include_dirs=self._config.include_dirs,
                gcc_args=self._config.gcc_args,
            )
            preproc.postprocess(i_file=i_file, out_file=p_file)
            system_headers.update(preproc.parse_system_header_paths(workdir / i_file))

        visitor = CpyVisitor(list(system_headers))

        for c_file in c_files:
            p_file = self._config.build_dir / f"{c_file.stem}.p"

            parser = c_ext.GnuCParser()
            ast = pycparser.parse_file(workdir / p_file, parser=parser)
            self.cleanup_parser_files()

            visitor.visit(ast)

        return ParserResults(visitor, c_files)

    @classmethod
    def cleanup_parser_files(cls, verbose: bool = True) -> None:
        # remove spurious PLY parser files after parsing
        yacctab_file = Path("yacctab.py")
        lextab_file = Path("lextab.py")
        if verbose:
            log.info(f"Removing spurious PLY parser file: {yacctab_file}")
            log.info(f"Removing spurious PLY parser file: {lextab_file}")
        yacctab_file.unlink(missing_ok=True)
        lextab_file.unlink(missing_ok=True)


class ParserResults:
    def __init__(self, visitor: CpyVisitor, local_c_files: list[Path]) -> None:
        ext_decls: list[c_ast.Decl] = visitor.get_external_called_decl(local_c_files)
        local_decls: list[c_ast.Decl] = visitor.get_local_func_decls(local_c_files)
        local_func_defs: list[c_ast.FuncDef] = visitor.get_local_func_defs()
        all_typedefs: list[Typeref] = visitor.get_all_typedefs()
        include_files: list[str] = visitor.get_include_files(local_c_files)

        log.debug(f"found {len(ext_decls)} external dependencies:")
        for ext_decl in ext_decls:
            log.debug(f"  {ext_decl.name} {ext_decl.coord}")

        log.debug(f"found {len(local_decls)} local definitions:")
        for local_decl in local_decls:
            log.debug(f"  {local_decl.name} {local_decl.coord}")

        self._all_cpy_types = [CpyType(typedef) for typedef in all_typedefs]
        self._include_files = include_files

        self._ext_cpy_funcs: dict[Path, list[CpyFunc]] = {}
        self._used_cpy_types: dict[Path, list[CpyType]] = {}
        for ext_decl in ext_decls:
            decl_file = Path(ext_decl.coord.file)
            cpy_func = CpyFunc(ext_decl, self._all_cpy_types)
            self._ext_cpy_funcs.setdefault(decl_file, []).append(cpy_func)

            if decl_file not in self._used_cpy_types:
                self._used_cpy_types[decl_file] = []

            for ext_type in cpy_func.get_all_types():
                for cpy_type in self._all_cpy_types:
                    if cpy_type.typedef.name == ext_type.names[0]:
                        CpyType.add_unique_type(self._used_cpy_types[decl_file], cpy_type)

        self._local_cpy_funcs: dict[Path, list[CpyFunc]] = {}
        for local_decl in local_decls:
            self._local_cpy_funcs.setdefault(Path(local_decl.coord.file), []).append(
                CpyFunc(local_decl, self._all_cpy_types)
            )

        self._local_cpy_func_defs: dict[Path, list[CpyFuncDef]] = {}
        for func_def in local_func_defs:
            self._local_cpy_func_defs.setdefault(Path(func_def.coord.file), []).append(
                CpyFuncDef(func_def, self._all_cpy_types, visitor)
            )

    @property
    def all_cpy_types(self) -> list[CpyType]:
        return self._all_cpy_types

    @property
    def ext_cpy_funcs(self) -> dict[Path, list[CpyFunc]]:
        return self._ext_cpy_funcs

    @property
    def local_cpy_funcs(self) -> dict[Path, list[CpyFunc]]:
        return self._local_cpy_funcs

    @property
    def local_cpy_func_defs(self) -> dict[Path, list[CpyFuncDef]]:
        return self._local_cpy_func_defs

    @property
    def used_cpy_types(self) -> dict[Path, list[CpyType]]:
        return self._used_cpy_types

    @property
    def include_files(self) -> list[str]:
        return list(self._include_files)
