import pytest

from ryon.hlir.yaml_dumper import hlir_to_yaml
from ryon.parser.yaml_loader import yaml_to_ast

from tests.data.code_fragments import fragments


@pytest.mark.parametrize("fragment", fragments)
def test_hlir(hlir_transformer, fragment):
    ast = yaml_to_ast(fragment.ast)
    actual_hlir = hlir_transformer.transform(ast)
    actual_hlir_yaml = hlir_to_yaml(actual_hlir)
    assert actual_hlir_yaml == fragment.hlir
