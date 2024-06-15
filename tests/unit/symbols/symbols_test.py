import pytest

from ryon.hlir.yaml_loader import yaml_to_hlir
from tests.data.code_fragments import fragments


@pytest.mark.parametrize("fragment", fragments)
def test_symbolizer(symbolizer, symbol_table, fragment):
    hlir = yaml_to_hlir(fragment.hlir)

    symbolizer.visit(hlir)

    assert symbol_table == fragment.symbol_table
