from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Mapping, Optional

from ryon.hlir.nodes import HLIRNode, ContextNode, TypeNode
from ryon.hlir.visitor import Visitor


@dataclass
class Symbol:
    type: Optional[TypeNode] = None


class SymbolTable(defaultdict[tuple[str, ...], Symbol]):
    def __init__(self, initial_items: Optional[Mapping[tuple[str, ...], Symbol]] = None):
        if initial_items is not None:
            super().__init__(Symbol, initial_items)
        else:
            super().__init__(Symbol)


class RyonSymbolizer(Visitor):
    def __init__(self, symbol_table: SymbolTable):
        self._table = symbol_table

    def arg(self, node, function, context):
        self._table[context + (node.name,)].type = node.type

    # def var(self, node, parent_data, context):
    #     yield
    #     yield

    def _transform_breadcrump(self, breadcrump: tuple[HLIRNode, ...]) -> Any:
        return tuple(node.get_context_name() for node in breadcrump if isinstance(node, ContextNode))
