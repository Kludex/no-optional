<h1 align="center">
    <strong>no-optional</strong>
</h1>
<p align="center">
    <a href="https://github.com/Kludex/no-optional" target="_blank">
        <img src="https://img.shields.io/github/last-commit/Kludex/no-optional" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/Kludex/no-optional/Test">
        <img src="https://img.shields.io/codecov/c/github/Kludex/no-optional">
    <br />
    <a href="https://pypi.org/project/no-optional" target="_blank">
        <img src="https://img.shields.io/pypi/v/no-optional" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/no-optional">
    <img src="https://img.shields.io/github/license/Kludex/no-optional">
</p>

This [codemod](https://libcst.readthedocs.io/en/stable/codemods_tutorial.html) replaces `typing.Optional[T]` by `typing.Union[T, None]` in the codebase.

## Installation

```bash
pip install no-optional
```

## Usage

Run the following on the repository you want to format:

```bash
python -m libcst.tool initialize .
```

Then, add the `no_optional` module to the `modules` list on the `.libcst.codemod.yaml` generated.

Then you are able to run:

```bash
python3 -m libcst.tool codemod main.NoOptionalCommand -j 1 <files>
```

## License

This project is licensed under the terms of the MIT license.
