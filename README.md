<h1 align="center">
    <strong>no-optional</strong>
</h1>
<p align="center">
    <a href="https://pypi.org/project/no-optional" target="_blank">
        <img src="https://img.shields.io/pypi/v/no-optional" alt="Package version">
    </a>
    <img src="https://img.shields.io/pypi/pyversions/no-optional">
    <img src="https://img.shields.io/github/license/Kludex/no-optional">
</p>

This [codemod](https://libcst.readthedocs.io/en/stable/codemods_tutorial.html) replaces `typing.Optional[T]` by `typing.Union[T, None]` in the codebase.

## Why?

This tool was inspired by a tweet from [Sebastián Ramírez](https://twitter.com/tiangolo) (as you see below), and a conversation between us.

<img width="599" alt="image" src="https://user-images.githubusercontent.com/7353520/173566552-6759f21e-e0d2-4bb6-9a7a-bac7c360e7fe.png">

As the tweet says, we have two reasons for doing this:

1. It's more explicit to write `Union[str, None]` than `Optional[str]`. Mainly because `Optional[str]` doesn't mean that the attribute is optional.
It only means that it accepts `None` as a possible value.
2. On Python 3.10+ you can type annotate as `str | None` instead of the above two. Which is more similar to `Union[str, None]` than `Optional[str]`.

## Installation

```bash
pip install no-optional
```

## Usage

Run the following on the repository you want to format:

```bash
python -m no_optional <files>
```

You can also use the pre-commit. Add the following to your `.pre-commit-config.yaml` file:

```yaml
  - repo: https://github.com/Kludex/no-optional
    rev: 0.4.0
    hooks:
      - id: no_optional
```

## License

This project is licensed under the terms of the MIT license.
