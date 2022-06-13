import inspect

import no_optional


def test_smoke() -> None:
    assert inspect.ismodule(no_optional)
