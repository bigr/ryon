import pytest

from ryon.hlir.yaml_dumper import hlir_to_yaml
from ryon.parser.yaml_loader import yaml_to_ast

from tests.data.code_fragments import fragments, NumberCodeFragment, NumberLiteralCodeFragment


@pytest.mark.parametrize("fragment", fragments)
def test_hlir(hlir_transformer, fragment):
    ast = yaml_to_ast(fragment.ast)
    actual_hlir = hlir_transformer.transform(ast)
    actual_hlir_yaml = hlir_to_yaml(actual_hlir)
    assert actual_hlir_yaml == fragment.hlir


@pytest.mark.parametrize(
    "number_type", ("I8", "I16", "I32", "I64", "I128", "U8", "U16", "U32", "U64", "U128", "F16", "F32", "F64")
)
def test_hlir_basic_numbers(hlir_transformer, number_type):
    fragment = NumberCodeFragment()
    ast = yaml_to_ast(fragment.ast(number_type))
    actual_hlir = hlir_transformer.transform(ast)
    actual_hlir_yaml = hlir_to_yaml(actual_hlir)
    assert actual_hlir_yaml == fragment.hlir(number_type)


@pytest.mark.parametrize("number_type", ("I8", "I16", "I32", "I64", "I128", "U8", "U16", "U32", "U64", "U128"))
def test_hlir_integer_literals(hlir_transformer, number_type):
    fragment = NumberLiteralCodeFragment()
    ast = yaml_to_ast(fragment.ast(number_type))
    actual_hlir = hlir_transformer.transform(ast)
    actual_hlir_yaml = hlir_to_yaml(actual_hlir)
    assert actual_hlir_yaml == fragment.hlir(number_type)
