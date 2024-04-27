from ctypes import CFUNCTYPE, c_void_p

import llvmlite.binding as llvm


def test_compiler(parser, compiler, tests_data_dir):
    content = open(tests_data_dir / "foo.ry").read()
    parsed_tree = parser.parse(content)

    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
    compiler.visit(parsed_tree)

    llvm_ir_parsed = llvm.parse_assembly(str(compiler.ir_module))
    llvm_ir_parsed.verify()

    target_machine = llvm.Target.from_default_triple().create_target_machine()
    engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
    engine.finalize_object()

    entry = engine.get_function_address("main")
    cfunc = CFUNCTYPE(c_void_p)(entry)

    assert cfunc() is None
