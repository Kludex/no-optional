from typing import List, Set

import libcst as cst
from libcst import ensure_type
from libcst import matchers as m
from libcst.codemod import VisitorBasedCodemodCommand

from no_optional.utils import is_typing_node


class NoOptionalCommand(VisitorBasedCodemodCommand):
    @m.leave(
        m.Subscript(
            value=m.Name(value="Optional")
            | m.Attribute(value=m.Name(value="typing"), attr=m.Name(value="Optional"))
        )
    )
    def replace_optional(
        self, original_node: cst.Subscript, updated_node: cst.Subscript
    ) -> cst.Subscript:
        if original_node.value.value == "Optional":
            union_type = cst.Name("Union")
        else:
            union_type = cst.Attribute(value=cst.Name("typing"), attr=cst.Name("Union"))

        return updated_node.with_changes(
            value=union_type,
            slice=[
                *updated_node.slice,
                cst.SubscriptElement(
                    slice=cst.Index(value=cst.Name("None")),
                    comma=cst.MaybeSentinel.DEFAULT,
                ),
            ],
        )

    @m.leave(
        m.Subscript(
            value=m.Name(value="Optional")
            | m.Attribute(value=m.Name("typing"), attr=m.Name("Optional")),
            slice=(
                m.SubscriptElement(
                    slice=m.Index(
                        value=m.Subscript(
                            value=m.Name(value="Union")
                            | m.Attribute(
                                value=m.Name(value="typing"), attr=m.Name(value="Union")
                            )
                        )
                    ),
                ),
                m.ZeroOrMore(),
            ),
        )
    )
    def remove_union_redundancy(
        self, original_node: cst.Subscript, updated_node: cst.Subscript
    ) -> cst.Subscript:
        return updated_node.with_changes(
            slice=[*updated_node.slice[0].slice.value.slice, *updated_node.slice[1:]]
        )

    @m.leave(
        m.Subscript(
            value=m.Name(value="Union")
            | m.Attribute(value=m.Name("typing"), attr=m.Name("Union")),
            slice=(
                m.ZeroOrMore(),
                m.SubscriptElement(
                    slice=m.Index(
                        value=m.Subscript(
                            value=m.Name(value="Optional")
                            | m.Attribute(
                                value=m.Name(value="typing"),
                                attr=m.Name(value="Optional"),
                            )
                        )
                    ),
                ),
                m.ZeroOrMore(),
            ),
        )
    )
    def remove_internal_optional(
        self, original_node: cst.Subscript, updated_node: cst.Subscript
    ) -> cst.Subscript:
        slices: List[cst.SubscriptElement] = []
        # 1. Iterate over slices, remove optional, and hold the inner slices
        for slice in updated_node.slice:
            if isinstance(slice.slice, cst.Index):
                value = slice.slice.value
                if isinstance(value, cst.Name):
                    slices.append(slice)
                elif isinstance(value, cst.Subscript):
                    slices.extend(value.slice)

        # 2. Compute unique slices
        unique_slices = []
        unique_names: Set[str] = set()
        for slice in slices:
            index = ensure_type(slice.slice, cst.Index)
            if isinstance(index.value, cst.Name):
                name = index.value.value
            elif isinstance(index.value, cst.Attribute):
                name = index.value.attr.value
            else:
                raise ValueError(f"Unexpected index type: {type(index.value)}")
            if name not in unique_names:
                unique_slices.append(slice)
                unique_names.add(name)

        # 3. Send `None` to the end
        unique_slices.sort(key=lambda x: is_typing_node(x.slice.value, "None"))

        return updated_node.with_changes(slice=unique_slices)

    @m.call_if_inside(m.ImportAlias(name=m.Name(value="Optional")))
    @m.leave(m.Name(value="Optional"))
    def replace_import(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> cst.Name:
        return updated_node.with_changes(value="Union")
