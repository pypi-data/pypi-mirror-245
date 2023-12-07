# CFug

Utilities for C++ project management.

## Requirements

- [CMake] >= 3.11
- [Git]

[CMake]: https://www.cmake.org
[Git]: https://git-scm.com/

## Commands

- `cfug new`: Initializes new project. By default header-only library template
  is used, but this can be changed with `--template` argument. Available
  templates are `header-only` and `library`.
- `cfug configure`: Runs CMake configuration on the project.
- `cfug build`: Builds the project.
- `cfug test`: Runs test cases.
- `cfug clean`: Cleans all build files.
