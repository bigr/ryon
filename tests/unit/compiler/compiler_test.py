import pytest
from ryon.hlir.yaml_loader import yaml_to_hlir

from ryon.compiler import RyonCompiler
from tests.data.code_fragments import fragments, NumberCodeFragment, NumberLiteralCodeFragment


def test_compiler_initialization():
    RyonCompiler()


@pytest.mark.parametrize("fragment", [f for f in fragments if f.hlir is not None])
def test_compiler(compiler, fragment):
    hlir = yaml_to_hlir(fragment.hlir)

    llvm_ir = compiler.visit(hlir)

    actual = llvm_ir[llvm_ir.find('target datalayout = ""') + 22 :].strip()

    assert actual == fragment.llvm_ir


@pytest.mark.parametrize(
    "number_type", ("I8", "I16", "I32", "I64", "I128", "U8", "U16", "U32", "U64", "U128", "F16", "F32", "F64")
)
def test_hlir_basic_numbers(compiler, number_type):
    fragment = NumberCodeFragment()

    hlir = yaml_to_hlir(fragment.hlir(number_type))
    llvm_ir = compiler.visit(hlir)
    actual = llvm_ir[llvm_ir.find('target datalayout = ""') + 22 :].strip()
    assert actual == fragment.llvm_ir(number_type)


@pytest.mark.parametrize("number_type", ("I8", "I16", "I32", "I64", "I128", "U8", "U16", "U32", "U64", "U128"))
def test_compiler_integer_literals(compiler, number_type):
    fragment = NumberLiteralCodeFragment()

    hlir = yaml_to_hlir(fragment.hlir(number_type))
    llvm_ir = compiler.visit(hlir)
    actual = llvm_ir[llvm_ir.find('target datalayout = ""') + 22 :].strip()
    assert actual == fragment.llvm_ir(number_type)
