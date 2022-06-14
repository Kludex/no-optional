import textwrap

import libcst as cst
import pytest
from libcst.codemod import CodemodContext

from no_optional import NoOptionalCommand


@pytest.mark.parametrize(
    "input,expected",
    (
        (
            textwrap.dedent(
                """
            from typing import Optional

            def function(a: Optional[int] = None) -> Optional[int]:
                ...
            """
            ),
            textwrap.dedent(
                """
            from typing import Union

            def function(a: Union[int, None] = None) -> Union[int, None]:
                ...
            """
            ),
        ),
        (
            textwrap.dedent(
                """
            import typing

            async def function(a: typing.Optional[int]) -> typing.Optional[int]:
                ...
            """
            ),
            textwrap.dedent(
                """
            import typing

            async def function(a: typing.Union[int, None]) -> typing.Union[int, None]:
                ...
            """
            ),
        ),
        (
            textwrap.dedent(
                """
            from typing import Optional

            class Potato:
                a: Optional[Union[int, str]]
            """
            ),
            textwrap.dedent(
                """
            from typing import Union

            class Potato:
                a: Union[int, str, None]
            """
            ),
        ),
        (
            textwrap.dedent(
                """
            a: int = 2
            """
            ),
            textwrap.dedent(
                """
            a: int = 2
            """
            ),
        ),
    ),
)
def test_transformer(input: str, expected: str) -> None:
    source_tree = cst.parse_module(input)
    print(source_tree)
    transformer = NoOptionalCommand(CodemodContext())
    modified_tree = source_tree.visit(transformer)
    assert modified_tree.code == expected
