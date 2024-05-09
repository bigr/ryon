import textwrap

from ryon.hlir.yaml_dumper import hlir_to_yaml

from ryon.hlir.nodes import Module, Fn, SimpleType, Return, Suite, DecimalNumber


def test_hlir_to_yaml():
    hlir = Module(
        module_statements=(
            Fn(
                name="test",
                type=SimpleType("I32"),
                args=(),
                body=Suite(statements=(Return(expression=DecimalNumber(5)),)),
            ),
        )
    )

    output = hlir_to_yaml(hlir)

    expected_output = textwrap.dedent("""
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
    """).strip()

    assert output.strip() == expected_output, "YAML output does not match expected"
