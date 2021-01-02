# Splatcoder
This Python package is similar to https://github.com/kyuridenamida/atcoder-tools but simpler version with fewer functionality.
If you happen to find this repository, please use the above `atcoder-tools` first since this is just for myself.

I also found a similar npm project. Google it.

## Installation
### Installing from pypi
This package is not registered at pypi.

### Installing from source
```sh
pip install .
# or
poetry build
pip install dist/splatcoder-<version>-py3-none-any.whl
```

## Usage
### start-contest
```sh
splat start-contest https://atcoder.jp/contests/abc174
# Or for short
splat c abc174
```

A directory named `abc174` will be splatted and it contains `x.cpp` for x in a, b, c, etc.

### start-task
```sh
splat start-task https://atcoder.jp/contests/abc174/tasks/abc174_a
# Or for short
splat t abc174/tasks/abc174_a
```

After this, you'll see a file named `abc174_a.cpp` splatted at the current directory.
If the name of the current directory is `abc174`, file name becomes `a.cpp`.


### check sample inputs
```sh
splat x.cpp
```

This builds the x.cpp file, executes it for the given test cases and the results will be splatted on the standard output.


## Configuration
Every splat command starts from reading config file that is located at `${HOME}/.splatconfig.yml` by default.
You can change the location by setting the environment variable `SPLAT_CONFIG_PATH`.

```yml
!splatcoder_config
build_command: "g++ -std=c++14"
template_path:
username: "pigimaru"
password: "xxxxxxxxxxxx"
```

Note that
* the first line is necessary for the yaml loader implemented at `splatcoder/config.py`.
* `username` and `password` are necessary for generating templates from the ongoing contest's page.
