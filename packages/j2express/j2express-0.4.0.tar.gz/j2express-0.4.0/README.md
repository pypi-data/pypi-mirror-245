# j2express
CLI for Jinja written from the ground up

# Motivation
This will provide more feedback than other implementations of j2 templating on the command line.

## Installation

After cloning the repo, activate a virtual environment and run

`pip install .`

## Running

Process template:

`j2x -f template.j2`

Show help and options:

`j2x --help`

### Flags

- `--trim-blocks / --no-trim-blocks`: Set Jinja's environment to trim whitespace. (default: --no-trim-blocks) 
- `--lstrip-blocks / --no-lstrip-blocks`: Set Jinja's environment to remove whitespace from the left. (default: --lstrip-blocks)

### Goals

- [X] process templates with exported env variables being represented as: `{{ VARIABLE_NAME }}`
- [X] install and make available on the command line
- [X] make available on PyPI
- [ ] colorized output for troubleshooting variables
- [ ] support for arrays from command line
