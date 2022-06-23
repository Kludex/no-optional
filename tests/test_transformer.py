import textwrap

import libcst as cst
import pytest
from libcst.codemod import CodemodContext

from no_optional import NoOptionalCommand


@pytest.mark.parametrize(
    "input,expected",
    (
        pytest.param(
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
        pytest.param(
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
        pytest.param(
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
        pytest.param(
            textwrap.dedent(
                """
            import typing

            class Potato:
                a: typing.Optional[typing.Union[int, str]]
            """
            ),
            textwrap.dedent(
                """
            import typing

            class Potato:
                a: typing.Union[int, str, None]
            """
            ),
        ),
        pytest.param(
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
        pytest.param(
            textwrap.dedent(
                """
            from typing import List, Optional

            def function(a: List[Optional[int]]) -> Optional[int]:
                ...
            """
            ),
            textwrap.dedent(
                """
            from typing import List, Union

            def function(a: List[Union[int, None]]) -> Union[int, None]:
                ...
            """
            ),
        ),
        pytest.param(
            textwrap.dedent(
                """
            from typing import Dict, Optional

            def function(a: Dict[str, Optional[int]]) -> Optional[int]:
                ...
            """
            ),
            textwrap.dedent(
                """
            from typing import Dict, Union

            def function(a: Dict[str, Union[int, None]]) -> Union[int, None]:
                ...
            """
            ),
        ),
        pytest.param(
            textwrap.dedent(
                """
            from typing import Optional, Union

            def function(a: Union[A, B, Optional[D], E, Optional[F]] = None):
                ...
            """
            ),
            textwrap.dedent(
                """
            from typing import Union

            def function(a: Union[A, B, D, E, F, None] = None):
                ...
            """
            ),
            marks=pytest.mark.skip("Not implemented"),
        ),
    ),
)
def test_transformer(input: str, expected: str) -> None:
    source_tree = cst.parse_module(input)
    print(source_tree)
    transformer = NoOptionalCommand(CodemodContext())
    modified_tree = source_tree.visit(transformer)
    assert modified_tree.code == expected
