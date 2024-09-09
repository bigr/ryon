import ctypes
from dataclasses import dataclass, field
import textwrap
from typing import Any, Type, Optional

from ryon.hlir.nodes import SimpleType
from ryon.symbols.symbols import SymbolTable, Symbol


@dataclass(frozen=True)
class Fragment:
    name: str
    code: str = field(repr=False)
    llvm_ir: str = field(repr=False)
    functions: tuple[tuple[str, Type, tuple[Any, ...], Any], ...] = field(repr=False)
    symbol_table: SymbolTable
    ast: Optional[str] = field(default=None, repr=False)
    hlir: Optional[str] = field(default=None, repr=False)

    def __post_init__(self):
        # Using object.__setattr__ to bypass the immutability for initialization
        object.__setattr__(self, "code", textwrap.dedent(self.code).strip() + "\n")

        if self.ast is not None:
            object.__setattr__(self, "ast", textwrap.dedent(self.ast).strip() + "\n")
        else:
            object.__setattr__(self, "ast", None)

        if self.hlir is not None:
            object.__setattr__(self, "hlir", textwrap.dedent(self.hlir).strip() + "\n")
        else:
            object.__setattr__(self, "hlir", None)

        object.__setattr__(self, "llvm_ir", textwrap.dedent(self.llvm_ir).strip())


fragments = [
    Fragment(
        name="Simple return",
        code="""
            fn hello_world() -> I32:
                return 10
        """,
        ast="""
            !Tree
            node: !Token 'RULE module'
            subtree:
            - !Tree
                node: !Token 'RULE function_definition'
                subtree:
                - !Token 'SNAKE_CASE_NAME hello_world'
                - null
                - !Tree
                    node: !Token 'RULE simple_type'
                    subtree:
                    - !Token 'UPPER_CAMEL_CASE_NAME I32'
                - !Tree
                    node: !Token 'RULE suite'
                    subtree:
                    - !Tree
                        node: !Token 'RULE return_statement'
                        subtree:
                        - !Tree
                            node: !Token 'RULE untyped_integer_literal'
                            subtree:
                            - !Token 'DECIMAL_NUMBER 10'
        """,
        hlir="""
            !node.Module
            module_statements:
            - !node.Fn
                name: hello_world
                type: !node.SimpleType
                    name: I32
                args: []
                body: !node.Suite
                    statements:
                    - !node.Return
                        expression: !node.UntypedIntegerLiteral
                            value: 10
        """,
        llvm_ir="""
            define i32 @"hello_world"()
            {
            entry:
              ret i32 10
            }
        """,
        functions=(("hello_world", ctypes.CFUNCTYPE(ctypes.c_void_p), (), 10),),
        symbol_table=SymbolTable(),
    ),
    Fragment(
        name="Add function",
        code="""
            fn add(a: I32, b: I32) -> I32:
                return a + b + 5
        """,
        ast="""
            !Tree
            node: !Token 'RULE module'
            subtree:
            - !Tree
                node: !Token 'RULE function_definition'
                subtree:
                - !Token 'SNAKE_CASE_NAME add'
                - !Tree
                    node: !Token 'RULE function_arguments'
                    subtree:
                    - !Tree
                        node: !Token 'RULE function_argument'
                        subtree:
                        - !Token 'SNAKE_CASE_NAME a'
                        - !Tree
                            node: !Token 'RULE simple_type'
                            subtree:
                            - !Token 'UPPER_CAMEL_CASE_NAME I32'
                    - !Tree
                        node: !Token 'RULE function_argument'
                        subtree:
                        - !Token 'SNAKE_CASE_NAME b'
                        - !Tree
                            node: !Token 'RULE simple_type'
                            subtree:
                            - !Token 'UPPER_CAMEL_CASE_NAME I32'
                - !Tree
                    node: !Token 'RULE simple_type'
                    subtree:
                    - !Token 'UPPER_CAMEL_CASE_NAME I32'
                - !Tree
                    node: !Token 'RULE suite'
                    subtree:
                    - !Tree
                        node: !Token 'RULE return_statement'
                        subtree:
                        - !Tree
                            node: !Token 'RULE summation'
                            subtree:
                            - !Tree
                                node: !Token 'RULE variable_identifier'
                                subtree:
                                - !Token 'SNAKE_CASE_NAME a'
                            - !Tree
                                node: !Token 'RULE variable_identifier'
                                subtree:
                                - !Token 'SNAKE_CASE_NAME b'
                            - !Tree
                                node: !Token 'RULE untyped_integer_literal'
                                subtree:
                                - !Token 'DECIMAL_NUMBER 5'
        """,
        hlir="""
            !node.Module
            module_statements:
            - !node.Fn
                name: add
                type: !node.SimpleType
                    name: I32
                args:
                - !node.Arg
                    name: a
                    type: !node.SimpleType
                        name: I32
                - !node.Arg
                    name: b
                    type: !node.SimpleType
                        name: I32
                body: !node.Suite
                    statements:
                    - !node.Return
                        expression: !node.Summation
                            addends:
                            - !node.Var
                                name: a
                                type: null
                            - !node.Var
                                name: b
                                type: null
                            - !node.UntypedIntegerLiteral
                                value: 5
        """,
        llvm_ir="""
            define i32 @"add"(i32 %"a", i32 %"b")
            {
            entry:
              %"result" = add i32 %"a", %"b"
              %"result.1" = add i32 %"result", 5
              ret i32 %"result.1"
            }
        """,
        functions=(("add", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int), (3, 4), 12),),
        symbol_table=SymbolTable(
            {
                ("add", "a"): Symbol(type=SimpleType(name="I32")),
                ("add", "b"): Symbol(type=SimpleType(name="I32")),
            }
        ),
    ),
]


class NumberCodeFragment:
    @staticmethod
    def code(number_type: str) -> str:
        code = f"""
            fn add(a: {number_type}, b: {number_type}) -> {number_type}:
                return a + b
        """

        return textwrap.dedent(code).strip() + "\n"

    @staticmethod
    def ast(number_type: str) -> str:
        ast = f"""
            !Tree
            node: !Token 'RULE module'
            subtree:
            - !Tree
                node: !Token 'RULE function_definition'
                subtree:
                - !Token 'SNAKE_CASE_NAME add'
                - !Tree
                    node: !Token 'RULE function_arguments'
                    subtree:
                    - !Tree
                        node: !Token 'RULE function_argument'
                        subtree:
                        - !Token 'SNAKE_CASE_NAME a'
                        - !Tree
                            node: !Token 'RULE simple_type'
                            subtree:
                            - !Token 'UPPER_CAMEL_CASE_NAME {number_type}'
                    - !Tree
                        node: !Token 'RULE function_argument'
                        subtree:
                        - !Token 'SNAKE_CASE_NAME b'
                        - !Tree
                            node: !Token 'RULE simple_type'
                            subtree:
                            - !Token 'UPPER_CAMEL_CASE_NAME {number_type}'
                - !Tree
                    node: !Token 'RULE simple_type'
                    subtree:
                    - !Token 'UPPER_CAMEL_CASE_NAME {number_type}'
                - !Tree
                    node: !Token 'RULE suite'
                    subtree:
                    - !Tree
                        node: !Token 'RULE return_statement'
                        subtree:
                        - !Tree
                            node: !Token 'RULE summation'
                            subtree:
                            - !Tree
                                node: !Token 'RULE variable_identifier'
                                subtree:
                                - !Token 'SNAKE_CASE_NAME a'
                            - !Tree
                                node: !Token 'RULE variable_identifier'
                                subtree:
                                - !Token 'SNAKE_CASE_NAME b'

        """

        return textwrap.dedent(ast).strip() + "\n"

    @staticmethod
    def hlir(number_type: str) -> str:
        hlir = f"""
            !node.Module
            module_statements:
            - !node.Fn
                name: add
                type: !node.SimpleType
                    name: {number_type}
                args:
                - !node.Arg
                    name: a
                    type: !node.SimpleType
                        name: {number_type}
                - !node.Arg
                    name: b
                    type: !node.SimpleType
                        name: {number_type}
                body: !node.Suite
                    statements:
                    - !node.Return
                        expression: !node.Summation
                            addends:
                            - !node.Var
                                name: a
                                type: null
                            - !node.Var
                                name: b
                                type: null
        """

        return textwrap.dedent(hlir).strip() + "\n"

    @staticmethod
    def llvm_ir(number_type: str) -> str:
        _CONV_TABLE = {"F16": "half", "F32": "float", "F64": "double"}

        if number_type in _CONV_TABLE:
            ntype = _CONV_TABLE[number_type]
        else:
            ntype = number_type.lower()
            if ntype[0] == "u":
                ntype = "i" + ntype[1:]

        llvm_ir = f"""
            define {ntype} @"add"({ntype} %"a", {ntype} %"b")
            {{
            entry:
              %"result" = add {ntype} %"a", %"b"
              ret {ntype} %"result"
            }}
        """

        return textwrap.dedent(llvm_ir).strip()


class NumberLiteralCodeFragment:
    @staticmethod
    def code(number_type: str) -> str:
        code = f"""
            fn foo() -> {number_type}:
                return 10:{number_type}
        """

        return textwrap.dedent(code).strip() + "\n"

    @staticmethod
    def ast(number_type: str) -> str:
        ast = f"""
            !Tree
            node: !Token 'RULE module'
            subtree:
            - !Tree
                node: !Token 'RULE function_definition'
                subtree:
                - !Token 'SNAKE_CASE_NAME foo'
                - null
                - !Tree
                    node: !Token 'RULE simple_type'
                    subtree:
                    - !Token 'UPPER_CAMEL_CASE_NAME {number_type}'
                - !Tree
                    node: !Token 'RULE suite'
                    subtree:
                    - !Tree
                        node: !Token 'RULE return_statement'
                        subtree:
                        - !Tree
                            node: !Token 'RULE typed_integer_literal'
                            subtree:
                            - !Token 'DECIMAL_NUMBER 10'
                            - !Tree
                                node: !Token 'RULE simple_type'
                                subtree:
                                - !Token 'UPPER_CAMEL_CASE_NAME {number_type}'
        """

        return textwrap.dedent(ast).strip() + "\n"

    @staticmethod
    def hlir(number_type: str) -> str:
        hlir = f"""
            !node.Module
            module_statements:
            - !node.Fn
                name: foo
                type: !node.SimpleType
                    name: {number_type}
                args: []
                body: !node.Suite
                    statements:
                    - !node.Return
                        expression: !node.TypedIntegerLiteral
                            value: 10
                            type: !node.SimpleType
                                name: {number_type}
        """

        return textwrap.dedent(hlir).strip() + "\n"

    @staticmethod
    def llvm_ir(number_type: str) -> str:
        _CONV_TABLE = {"F16": "half", "F32": "float", "F64": "double"}

        if number_type in _CONV_TABLE:
            ntype = _CONV_TABLE[number_type]
        else:
            ntype = number_type.lower()
            if ntype[0] == "u":
                ntype = "i" + ntype[1:]

        llvm_ir = f"""
            define {ntype} @"foo"()
            {{
            entry:
              ret {ntype} 10
            }}
        """

        return textwrap.dedent(llvm_ir).strip()
