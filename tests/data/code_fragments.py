from dataclasses import dataclass, field
import textwrap


@dataclass(frozen=True)
class Fragment:
    name: str
    code: str = field(repr=False)
    ast: str = field(repr=False)

    def __post_init__(self):
        # Using object.__setattr__ to bypass the immutability for initialization
        object.__setattr__(self, "code", textwrap.dedent(self.code).strip() + "\n")
        object.__setattr__(self, "ast", textwrap.dedent(self.ast).strip() + "\n")


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
    ),
]
