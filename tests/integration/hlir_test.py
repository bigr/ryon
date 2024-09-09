import pytest

from ryon.hlir.yaml_loader import yaml_to_hlir
from ryon.parser.yaml_loader import yaml_to_ast

from ryon.hlir.yaml_dumper import hlir_to_yaml
from tests.data.code_fragments import fragments


@pytest.mark.parametrize("fragment", [f for f in fragments if f.hlir is not None])
def test_yaml(hlir_transformer, fragment):
    ast = yaml_to_ast(fragment.ast)
    expected_hlir = hlir_transformer.transform(ast)

    actual_hlir_yaml = hlir_to_yaml(expected_hlir)
    assert actual_hlir_yaml == fragment.hlir

    actual_hlir = yaml_to_hlir(actual_hlir_yaml)

    assert actual_hlir == expected_hlir
