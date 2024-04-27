from lark import Visitor
import llvmlite.binding as llvm
from llvmlite import ir


class RyonCompiler(Visitor):
    def __init__(self):
        self.ir_module = ir.Module(name="main_module")
        self.ir_module.triple = llvm.get_default_triple()
        self.builder = None

    def module(self, node):
        func_type = ir.FunctionType(ir.VoidType(), [])
        main_function = ir.Function(self.ir_module, func_type, name="main")
        block = main_function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.builder.ret_void()
