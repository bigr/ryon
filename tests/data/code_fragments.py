from dataclasses import dataclass, field
import textwrap


@dataclass(frozen=True)
class Fragment:
    name: str
    code: str = field(repr=False)
    ast: str = field(repr=False)
    hlir: str = field(repr=False)
    llvm_ir: str = field(repr=False)

    def __post_init__(self):
        # Using object.__setattr__ to bypass the immutability for initialization
        object.__setattr__(self, "code", textwrap.dedent(self.code).strip() + "\n")
        object.__setattr__(self, "ast", textwrap.dedent(self.ast).strip() + "\n")
        object.__setattr__(self, "hlir", textwrap.dedent(self.hlir).strip() + "\n")
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
                        expression: !node.DecimalNumber
                            value: 10
        """,
        llvm_ir="""
            define i32 @"hello_world"()
            {
            entry:
              ret i32 10
            }
        """,
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
                            - !node.DecimalNumber
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
    ),
]
