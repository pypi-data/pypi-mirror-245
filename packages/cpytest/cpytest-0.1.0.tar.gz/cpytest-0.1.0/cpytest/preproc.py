"""Utility module for preprocessing C files using gcc."""

import os
from pathlib import Path
import re
import subprocess
from typing import Sequence

import regex

from cpytest import logger


log = logger.setup_logger("preproc")


class Preproc:
    def __init__(self, workdir: Path | None = None):
        if workdir is None:
            workdir = Path.cwd()
        else:
            assert isinstance(workdir, Path)
            assert workdir.is_dir(), f"workdir not found: {workdir}"
        self._workdir = workdir

    def _workdir_path(self, file: Path) -> Path:
        assert isinstance(file, Path)
        if file.is_absolute():
            return file
        return self._workdir / file

    def preprocess(
        self,
        c_file: Path,
        outfile: Path,
        incl_rel_dir: Path,
        include_dirs: Sequence[Path] | None = None,
        gcc_args: Sequence[str] | None = None,
    ) -> None:
        """Preprocess a C file using gcc.

        c_file: The C file to preprocess. Absolute or relative to the workdir.
        outfile: The output file. Absolute or relative to the workdir.
        """
        assert c_file is not None
        assert outfile is not None
        assert incl_rel_dir is not None

        assert self._workdir_path(c_file).is_file(), f"file not found: {self._workdir_path(c_file)}"

        outfile_wd = self._workdir_path(outfile)

        log.info(f"Preprocessing... workdir: {self._workdir}")
        log.debug(f"c_file:       {c_file}")
        log.debug(f"outfile:      {outfile_wd}")
        log.debug(f"incl_rel_dir: {incl_rel_dir}")

        self._workdir.mkdir(parents=True, exist_ok=True)
        outfile_wd.parent.mkdir(parents=True, exist_ok=True)

        include_dirs_strs = set()
        for include_dir in include_dirs or []:
            assert isinstance(include_dir, Path)
            if include_dir.is_absolute():
                include_path = str(include_dir)
            else:
                include_path = os.path.normpath(incl_rel_dir / include_dir)
            include_dirs_strs.add(f"-I{include_path}")

        include_dirs_str = " ".join(include_dirs_strs)
        gcc_args_str = " ".join(gcc_args or [])

        gcc_cmd = f"gcc -E {c_file} {gcc_args_str} {include_dirs_str} -o {outfile}"
        log.debug(f"{gcc_cmd}")
        subprocess.run(gcc_cmd, cwd=self._workdir, shell=True, check=True)
        assert outfile_wd.is_file(), f"failed to preprocess. Outfile wasn't created: {outfile_wd}"
        log.info(f"generated preprocessor output: {outfile_wd}")

    @classmethod
    def _replace_all_gcc_attributes(cls, input_str: str) -> str:
        """Replace all GCC attributes with the same number of newlines as the attribute had."""
        assert input_str is not None

        def replace_with_newlines(match: regex.Match) -> str:
            newline_count = str(match.group()).count('\n')
            return '\n' * newline_count

        # https://regex101.com/r/jGGgAt/1
        rgx = r"__attribute__\s*(\(((?>[^\(\)]+|(?1))*)\))"
        return regex.sub(rgx, replace_with_newlines, input_str)

    def postprocess(self, i_file: Path, out_file: Path) -> None:
        """Postprocess a preprocessed C file.

        Remove all GCC directives from the preprocessed file and write the result to the output file.
        """
        assert i_file is not None
        assert out_file is not None

        assert isinstance(i_file, Path)
        assert isinstance(out_file, Path)

        assert self._workdir_path(i_file).is_file(), f"input file not found: {self._workdir_path(i_file)}"

        outfile_wd = self._workdir_path(out_file)
        outfile_wd.parent.mkdir(parents=True, exist_ok=True)

        log.info(f"postprocessing: {self._workdir_path(i_file)} -> {outfile_wd}")

        with self._workdir_path(i_file).open('r', encoding='UTF-8') as infile:
            with outfile_wd.open('w', encoding='UTF-8') as outfile:
                input_str = infile.read()
                output_str = self._replace_all_gcc_attributes(input_str)
                outfile.write(output_str)

    @classmethod
    def parse_system_header_paths(cls, i_file: Path) -> set[Path]:
        """Return a list of system headers that are included in the preprocessed file.

        Read the preprocessed file and search for GCC preprocessor linemarkers, as specified in:
            https://gcc.gnu.org/onlinedocs/cpp/Preprocessor-Output.html

        Regex:
            https://regex101.com/r/oAWlZG/1
        """
        assert i_file is not None
        assert isinstance(i_file, Path)

        pattern = re.compile(r"#\s+(?P<linenum>\d+)\s+\"(?P<filename>[^\"]*)\"(?P<flags>(\s+[1-4])*)")
        system_headers = set()
        non_system_headers = set()
        with open(i_file, 'r', encoding='UTF-8') as file:
            for line in file:
                match = pattern.match(line)
                if match:
                    filename = Path(match.group('filename'))
                    if "3" in match.group('flags'):
                        system_headers.add(filename)
                    else:
                        non_system_headers.add(filename)
        # In some cases, non-system headers are also flagged as "3 4", i.e. when a "bool" type is resolved from "_Bool".
        # For these cases, we remove the non-system headers from the system headers.
        system_headers -= non_system_headers
        return system_headers
