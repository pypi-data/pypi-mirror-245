```sh
sudo apt install gcovr
sudo apt insall lcov

virtualenv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

./clean

python3 test/build_example.py
pytest test/test_example.py

lcov --capture --directory src --base-directory test/build --output-file coverage.info --rc lcov_branch_coverage=1 --no-external
genhtml coverage.info --output-directory coverage_report --rc genhtml_branch_coverage=1

# for gcovr to work, we'd need to change the cffi compilation location to be on the project root folder. otherwise
# it can't follow the relative paths, which are pointing from test/build
gcovr --root . --html --html-details -o coverage.html

```


# cPyGen

```sh
# preprocess
gcc -E -Iinc src/example.c -o test/build/example.i
# generate
python3 cpygen.py
```

The `cpygen.py` is an experiment using `pycparser`. In order to parse GCC specific extensions, `pycparserext` is used.

`pycparser` is supposed to run on preprocessed C code.

Important to install in this order, because of version incompatibilities. `pycparserext==2021.1` depends on `pycparser==2.20`, but we need `pycparser==2.21`. The corresponding `pip install` error can be ignored.

Unfortunately, the `pycparsext` project is quite incomplete. `__attribue__(())` directives on structs are not supported. As an alternative for such cases, the `#pragma pack` needs to be used so that we're able to process packed structs. Processing packed structs is important, because we have to generate specific python code for them.

## Dependencies

```sh
pip install pycparserext==2021.1
pip install pycparser==2.21
```


### Running (new)
```sh
./clean.sh
py cpytest/cpygen.py
py example/test/build_example.py
pytest example/test/test_example.py
lcov --capture --directory example/src --base-directory example/test/builds --output-file coverage.info --rc lcov_branch_coverage=1 --no-external
genhtml coverage.info --output-directory coverage_report --rc genhtml_branch_coverage=1
```

### Running (manual steps) (old)

```sh
./clean.sh
mkdir example/test/build
# preprocess source file
gcc -E -Iexample/inc example/src/example.c -o example/test/build/example.i
# generate cffi python stubs into "out.c/out.h"
python3 cpytest/cpygen.py
# manual step: update "test/build_example.py": copy code from "out.c" and "out.h" into the test file
# compile the source file with generated stubs, and create the cffi python module
python3 test/build_example.py
# run the python unit tests against the compiled source
pytest test/test_example.py
```

### Run QA
```sh
pytest test/test_cpygen.py
flake8 --max-line-length 120 cpytest/cpygen.py test/test_cpygen.py example/test/build_example.py
pylint --max-line-length 120 cpytest/cpygen.py
```


### Docker

```sh
cd docker
docker-compose up --build test-example-project

docker-compose up -d shell
docker-compose exec shell bash

docker-compose down
```
