from lark import Transformer

from ryon.hlir.nodes import Fn, SimpleType, Arg, Suite, Return, Summation, Module, Var, UntypedIntegerLiteral


class HLIRTransformer(Transformer):
    def __init__(self):
        pass

    def module(self, node):
        return Module(module_statements=tuple(node))

    def function_definition(self, node):
        function_name, arguments, return_type, suite = node

        return Fn(name=function_name, type=return_type, args=arguments if arguments is not None else (), body=suite)

    def suite(self, node):
        return Suite(statements=tuple(node))

    def return_statement(self, node):
        return Return(expression=node[0])

    def summation(self, node):
        return Summation(addends=tuple(node))

    def untyped_integer_literal(self, node):
        return UntypedIntegerLiteral(node[0])

    def DECIMAL_NUMBER(self, node):
        return int(node.value)

    def function_argument(self, node):
        return Arg(name=node[0], type=node[1])

    def function_arguments(self, node):
        return tuple(node)

    def simple_type(self, node):
        return SimpleType(name=node[0])

    def UPPER_CAMEL_CASE_NAME(self, node):
        return node.value

    def variable_identifier(self, node):
        return Var(name=node[0], type=None)

    def SNAKE_CASE_NAME(self, node):
        return node.value
