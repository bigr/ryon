from llvmlite import ir

from ryon.hlir.visitor import Visitor


class RyonCompiler(Visitor):
    def __init__(self):
        pass

    def module(self, node, parent_data, breadcrump):
        module = ir.Module(name="simple_module")
        yield module
        yield str(module)

    def fn(self, node, module, breadcrump):
        function_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32)] * len(node.args))
        function = ir.Function(module, function_type, name=node.name)
        for arg, node_arg in zip(function.args, node.args):
            arg.name = node_arg.name
        yield function

    def suite(self, node, function, breadcrump):
        block = function.append_basic_block(name="entry")
        builder = ir.IRBuilder(block)
        yield builder, function

    def return_(self, node, parent_data, breadcrump):
        builder, function = parent_data

        child_nodes = yield builder, function
        expression = child_nodes["expression"]
        builder.ret(expression)

    def summation(self, node, parent_data, breadcrump):
        builder, function = parent_data
        child_nodes = yield builder, function
        addends = child_nodes["addends"]
        sum_result = addends[0]
        for addend in addends[1:]:
            sum_result = builder.add(sum_result, addend, name="result")
        yield sum_result

    def var(self, node, parent_data, breadcrump):
        builder, function = parent_data
        yield
        yield next(arg for arg in function.args if arg.name == node.name)

    def decimal_number(self, node, parent_data, breadcrump):
        builder, _ = parent_data
        yield
        yield ir.Constant(ir.IntType(32), int(node.value))
