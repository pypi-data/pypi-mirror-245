# sm2mpx

![coverage](https://gitlab.com/Menschel/sm2mpx/badges/master/coverage.svg)
![pipeline](https://gitlab.com/Menschel/sm2mpx/badges/master/pipeline.svg)

[Documentation](https://menschel.gitlab.io/sm2mpx/)


A python 3 unpacker for SM2MPX files , a proprietary format used by H-Games from the late 90's.
Filenames SE, VOICE, GGD, DATA are a clear indicator that it is this format.

# Description

Create an unpacker utility for this format to extract contents, just for fun.

# Usage

This utility copy's a shell executable to your local bin folder, so you can call it directly.
```
$ sm2mpx -h
usage: sm2mpx [-h] [-l] [-e] [-o OUTPUT_BASE_DIR] file

positional arguments:
  file                A .bf file or a directory with .bf files.

optional arguments:
  -h, --help          show this help message and exit
  -l                  A flag to list the contents of FILE.
  -e                  A flag to extract the contents of FILE.
  -o OUTPUT_BASE_DIR  The output base directory where to extract to, defaults
                      to current working directory.
```

# Deprecation of PyPi Packages
Packages on PyPi are no longer updated due to attempts of the Python Software Foundation to enforce new rules and basically flush out 
developers who do not consent.  
Recent packages can be installed directly from git, i.e.   
```pip install git+https://gitlab.com/Menschel/sm2mpx.git --upgrade```
