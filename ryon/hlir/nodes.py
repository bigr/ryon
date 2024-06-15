from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class HLIRNode:
    pass


@dataclass(frozen=True)
class ContextNode(ABC, HLIRNode):
    @abstractmethod
    def get_context_name(self):
        pass


@dataclass(frozen=True)
class TypeNode(HLIRNode):
    pass


@dataclass(frozen=True)
class SimpleType(TypeNode):
    name: str


@dataclass(frozen=True)
class Arg(HLIRNode):
    name: str
    type: TypeNode


@dataclass(frozen=True)
class Var(HLIRNode):
    name: str
    type: Optional[TypeNode]


@dataclass(frozen=True)
class LiteralNode(HLIRNode):
    pass


@dataclass(frozen=True)
class DecimalNumber(LiteralNode):
    value: int


@dataclass(frozen=True)
class ExpressionNode(HLIRNode):
    pass


@dataclass(frozen=True)
class Summation(ExpressionNode):
    addends: tuple[ExpressionNode | LiteralNode | Var, ...]


@dataclass(frozen=True)
class StatementNode(HLIRNode):
    pass


@dataclass(frozen=True)
class Return(StatementNode):
    expression: ExpressionNode | LiteralNode


@dataclass(frozen=True)
class Suite(HLIRNode):
    statements: tuple[StatementNode, ...]


@dataclass(frozen=True)
class Fn(ContextNode):
    name: str
    type: TypeNode
    args: tuple[Arg, ...]
    body: Suite

    def get_context_name(self):
        return self.name


@dataclass(frozen=True)
class Module(HLIRNode):
    module_statements: tuple[Fn, ...]
