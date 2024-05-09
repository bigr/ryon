from ryon.hlir.nodes import HLIRNode

from ryon.hlir.yaml_loader import yaml_to_hlir

from ryon.hlir.nodes import Module, Fn, SimpleType, Return, Suite, DecimalNumber


def test_yaml_to_hlir():
    yaml_data = """
        !node.Module
        module_statements:
        - !node.Fn
            name: test
            type: !node.SimpleType
                name: I32
            args: []
            body: !node.Suite
                statements:
                - !node.Return
                    expression: !node.DecimalNumber
                        value: 5
    """
    actual = yaml_to_hlir(yaml_data)
    assert isinstance(actual, HLIRNode)
    expected = Module(
        module_statements=(
            Fn(
                name="test",
                type=SimpleType("I32"),
                args=(),
                body=Suite(statements=(Return(expression=DecimalNumber(5)),)),
            ),
        )
    )

    assert actual == expected
