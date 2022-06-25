from typing import Union

import libcst as cst


def is_typing_node(node: Union[cst.Name, cst.Attribute], name: str) -> bool:
    if isinstance(node, cst.Name):
        return node.value == name
    else:
        return node.value == "typing" and node.attr.value == name
