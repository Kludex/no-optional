import libcst as cst
from libcst import matchers as m
from libcst.codemod import VisitorBasedCodemodCommand


class NoOptionalCommand(VisitorBasedCodemodCommand):
    @m.call_if_inside(
        m.Annotation(
            annotation=m.Subscript(
                value=m.Name(value="Optional")
                | m.Attribute(
                    value=m.Name(value="typing"), attr=m.Name(value="Optional")
                )
            )
        )
    )
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
            return updated_node.with_changes(
                value=cst.Name("Union"),
                slice=[
                    *updated_node.slice,
                    cst.SubscriptElement(
                        slice=cst.Index(value=cst.Name("None")),
                        comma=cst.MaybeSentinel.DEFAULT,
                    ),
                ],
            )
        else:
            return updated_node.with_changes(
                value=cst.Attribute(value=cst.Name("typing"), attr=cst.Name("Union")),
                slice=[
                    *updated_node.slice,
                    cst.SubscriptElement(
                        slice=cst.Index(value=cst.Name("None")),
                        comma=cst.MaybeSentinel.DEFAULT,
                    ),
                ],
            )

    @m.call_if_inside(
        m.Annotation(
            annotation=m.Subscript(
                value=m.Name(value="Optional")
                | m.Attribute(value=m.Name("typing"), attr=m.Name("Optional")),
                slice=(
                    m.SubscriptElement(
                        slice=m.Index(value=m.Subscript(value=m.Name(value="Union"))),
                    ),
                    m.ZeroOrMore(),
                ),
            )
        )
    )
    @m.leave(
        m.Subscript(
            value=m.Name(value="Optional")
            | m.Attribute(value=m.Name("typing"), attr=m.Name("Optional"))
        )
    )
    def remove_union_redundancy(
        self, original_node: cst.Subscript, updated_node: cst.Subscript
    ) -> cst.Subscript:
        return updated_node.with_changes(
            slice=[*updated_node.slice[0].slice.value.slice, *updated_node.slice[1:]]
        )

    @m.call_if_inside(m.ImportAlias(name=m.Name(value="Optional")))
    @m.leave(m.Name(value="Optional"))
    def replace_import(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> cst.Name:
        return updated_node.with_changes(value="Union")
