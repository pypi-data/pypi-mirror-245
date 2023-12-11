#!/usr/bin/env python3

"""
dependencies:
    pycparser==2.21
    pycparserext==2021.1

This will show conflicting versions, but it is okay.

pycparser 2.21 is needed, because it supports "_Static_assert()".
pycparserext 2021.1 depends on 2.20, but also seems to work with 2.21.


TODOs:

- [x] generate python stubs for external functions
- [x] remaining types from real source files
- [x] integrate preprocessor
    - [ ] check gcc path
- [x] multiple source files
    - [x] python stub file for each external linkage
    - [-] move compiled *.so file next to python stubs, to make it clearer and easier to import
- [x] yaml configuration file
- [ ] CLI to inspect the C file, such as listing functions and types
- [ ] add error for function calls, which are not found anywhere? currently there is only a warning when compiling cffi
- [x] logging no printing
- [x] option to generate empty test_module.py file
- [ ] consider compiling and building test with test execution. e.g. add a pytest fixture, which compiles the test
      unit and loads the library
    - [ ] store hash of preprocessed files, to avoid recompiling
- [-] investigate handling sys.exit() or segfault -> not easily possible
- [x] generate blank test case for each function
- [ ] in postpreprocessing, add a warning when removing __attribute__((packed))

Details:
- [x] support bool/_Bool type
- [x] bit fields
- [x] fix generating complex enum identifiers, which are not supported by cffi

"""
from pathlib import Path
import sys

from cpytest.parse import Parser
from cpytest.codegen import CodeGenerator
from cpytest import logger
from cpytest.config import Config
from cpytest.cpyffi import CpyFfiBuilder


log = logger.setup_logger("main")


def main() -> None:
    if len(sys.argv) > 1:
        yaml_file = Path(sys.argv[1])
    else:
        yaml_file = Path(__file__).parent.parent / "example" / "test" / "cpytest.yaml"

    config = Config(yaml_file)

    workdir = config.project_dir
    build_dir = workdir / config.build_dir
    py_stubs_dir = config.py_stubs_dir

    build_dir.mkdir(parents=True, exist_ok=True)
    py_stubs_dir.mkdir(parents=True, exist_ok=True)

    log.info(f"parsing c file: {config.c_files}")
    cpy_parser = Parser(config)
    parse_results = cpy_parser.parse()

    code_gen = CodeGenerator(config, parse_results)

    cffi_c_file_name = config.unit_name + "_cffi.c"
    cffi_h_file_name = config.unit_name + "_cffi.h"
    cffi_c_file = build_dir / cffi_c_file_name
    cffi_h_file = build_dir / cffi_h_file_name

    log.info(f"generating cffi C source: {cffi_c_file}")
    code_gen.gen_cpy_source_file(cffi_c_file)
    log.info(f"generating cffi C definitions: {cffi_h_file}")
    code_gen.gen_cpy_header_file(cffi_h_file)

    log.info("compiling cffi test unit ...")
    cpyffi = CpyFfiBuilder(config)
    cpyffi.compile(cffi_c_file, cffi_h_file)

    log.info(f"generating python stub: {py_stubs_dir}")
    stub_files = code_gen.gen_cpy_py_stub_files(py_stubs_dir)

    pytest_template_file = workdir / Path(f"test_{config.unit_name}_template.py")
    log.info(f"generating pytest stub: {pytest_template_file}")
    code_gen.gen_pytest_template(pytest_template_file)

    log.info("formatting generated files ...")
    code_gen.format_py_files([pytest_template_file] + stub_files)

    log.info("done")


if __name__ == "__main__":
    main()
