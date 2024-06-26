import pytest
from ryon.hlir.yaml_loader import yaml_to_hlir

from ryon.compiler import RyonCompiler
from tests.data.code_fragments import fragments


def test_compiler_initialization():
    RyonCompiler()


@pytest.mark.parametrize("fragment", fragments)
def test_compiler(compiler, fragment):
    hlir = yaml_to_hlir(fragment.hlir)

    llvm_ir = compiler.visit(hlir)

    actual = llvm_ir[llvm_ir.find('target datalayout = ""') + 22 :].strip()

    assert actual == fragment.llvm_ir
