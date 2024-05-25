import pytest
from ryon.hlir.nodes import SimpleType, Suite, Return, DecimalNumber, Fn, Arg, Summation, Var

from ryon.hlir.yaml_loader import yaml_to_hlir

from ryon.hlir.visitor import Visitor
from tests.data.code_fragments import fragments


@pytest.mark.parametrize(
    "fragment, call_count, calls",
    zip(
        fragments,
        (1, 3),
        (
            [(SimpleType(name="I32"), "Fn")],
            [
                (SimpleType(name="I32"), "Fn"),
                (SimpleType(name="I32"), "Arg"),
                (SimpleType(name="I32"), "Arg"),
            ],
        ),
    ),
)
def test_visit_simple_node(fragment, call_count, calls):
    hlir = yaml_to_hlir(fragment.hlir)

    class TestVisitor(Visitor):
        def __init__(self):
            self.call_count = 0
            self.calls = []

        def simple_type(self, node, children_data, breadcrump):
            self.call_count += 1
            self.calls.append((node, children_data))

        def __default__(self, node, children_data, breadcrump):
            return node.__class__.__name__

    visitor = TestVisitor()
    result = visitor.visit(hlir)

    assert visitor.call_count == call_count
    assert visitor.calls == calls

    assert result == "Module"


@pytest.mark.parametrize(
    "fragment, call_count, calls, children_data",
    zip(
        fragments,
        (1, 1),
        (
            [
                (
                    Fn(
                        name="hello_world",
                        type=SimpleType(name="I32"),
                        args=(),
                        body=Suite(statements=(Return(expression=DecimalNumber(value=10)),)),
                    ),
                    "This is module",
                    ("Module",),
                ),
            ],
            [
                (
                    Fn(
                        name="add",
                        type=SimpleType(name="I32"),
                        args=(
                            Arg(name="a", type=SimpleType(name="I32")),
                            Arg(name="b", type=SimpleType(name="I32")),
                        ),
                        body=Suite(
                            statements=(
                                Return(
                                    expression=Summation(
                                        addends=(
                                            Var(name="a", type=None),
                                            Var(name="b", type=None),
                                            DecimalNumber(value=5),
                                        )
                                    )
                                ),
                            )
                        ),
                    ),
                    "This is module",
                    ("Module",),
                )
            ],
        ),
        (
            [{"args": (), "body": "Suite", "name": "hello_world", "type": "SimpleType"}],
            [{"args": ("Arg", "Arg"), "body": "Suite", "name": "add", "type": "SimpleType"}],
        ),
    ),
)
def test_visit_complex_node(fragment, call_count, calls, children_data):
    hlir = yaml_to_hlir(fragment.hlir)

    class TestVisitor(Visitor):
        def __init__(self):
            self.call_count = 0
            self.calls = []
            self.children_data = []

        def fn(self, node, parent_data, breadcrump):
            self.call_count += 1
            self.calls.append((node, parent_data, breadcrump))

            children_data = yield node.name
            self.children_data.append(children_data)

        def module(self, node, parent_data, breadcrump):
            yield "This is module"
            yield "This is module - final"

        def __default__(self, node, parent_data, breadcrump):
            return node.__class__.__name__

        def _transform_breadcrump(self, breadcrump):
            return tuple(b.__class__.__name__ for b in breadcrump)

    visitor = TestVisitor()
    result = visitor.visit(hlir)

    assert visitor.call_count == call_count
    assert visitor.calls == calls
    assert visitor.children_data == children_data

    assert result == "This is module - final"
