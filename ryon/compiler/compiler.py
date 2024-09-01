from llvmlite import ir

from ryon.hlir.visitor import Visitor


class RyonCompiler(Visitor):
    _TYPE_MAPPING = {
        "I8": ir.IntType(8),
        "I16": ir.IntType(16),
        "I32": ir.IntType(32),
        "I64": ir.IntType(64),
        "I128": ir.IntType(128),
        "U8": ir.IntType(8),
        "U16": ir.IntType(16),
        "U32": ir.IntType(32),
        "U64": ir.IntType(64),
        "U128": ir.IntType(128),
        "F16": ir.HalfType(),
        "F32": ir.FloatType(),
        "F64": ir.DoubleType(),
    }

    def __init__(self):
        pass

    def module(self, node, parent_data, breadcrump):
        module = ir.Module(name="simple_module")
        yield module
        yield str(module)

    def fn(self, node, module, breadcrump):
        function_type = ir.FunctionType(
            self._TYPE_MAPPING[node.type.name], [self._TYPE_MAPPING[node_arg.type.name] for node_arg in node.args]
        )
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
