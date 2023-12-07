"""The head component."""

from nextpy.frontend.components.component import Component


class NextHeadLib(Component):
    """Header components."""

    library = "next/head"


class Head(NextHeadLib):
    """Head Component."""

    tag = "NextHead"

    is_default = True
