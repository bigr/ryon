import llvmlite.binding as llvm
import pytest

from tests.data.code_fragments import fragments


@pytest.fixture
def init_llvm():
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()


@pytest.mark.parametrize("fragment", fragments)
def test_compiler(parser, hlir_transformer, compiler, init_llvm, fragment):
    ast = parser.parse(fragment.code)
    hlir = hlir_transformer.transform(ast)
    module = compiler.visit(hlir)

    compiled_module = llvm.parse_assembly(str(module))
    compiled_module.verify()

    llvm_ir = compiler.visit(hlir)
    actual = llvm_ir[llvm_ir.find('target datalayout = ""') + 22 :].strip()
    assert actual == fragment.llvm_ir

    target_machine = llvm.Target.from_default_triple().create_target_machine()
    engine = llvm.create_mcjit_compiler(compiled_module, target_machine)
    engine.finalize_object()

    for name, cfunc, args, expected_return in fragment.functions:
        entry = engine.get_function_address(name)

        assert cfunc(entry)(*args) == expected_return
