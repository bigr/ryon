import inspect
import keyword
import re
from dataclasses import fields
from typing import Any, Dict, Optional

from ryon.hlir.nodes import HLIRNode


class Visitor:
    """
    Provides a mechanism for traversing and optionally transforming HLIR tree nodes.

    This class manages the recursive visiting of each node in the high-level intermediate representation (HLIR)
    tree of the 'ryon' language. The traversal process involves:

    1. Identifying the corresponding visit method based on the node's type, which is named in snake_case.
    2. Invoking the visit method with the node as an argument.
    3. Utilizing generator functions in visit methods to facilitate both top-down and bottom-up traversal.
       This allows initial processing before and further actions after the traversal of child nodes,
       incorporating parent data where applicable.
    4. Processing child nodes recursively, enabling modifications to be applied to the node from the yield point onward.

    Methods corresponding to the HLIRNode types should be implemented in subclasses, and can either be regular or
    generator methods depending on the desired flow of data and control.

    Example:
        class MyVisitor(Visitor):
            def visit_binary_expression_node(self, node, parent_data):
                # Pre-yield processing (top-down)
                do_something_with_node_before_child_visit(node)
                node_data = transform_node(node)

                # Yield control and send node data to allow child processing
                children_data = yield node_data

                # Post-yield processing (bottom-up)
                do_something_with_node_after_child_visit(node, children_data)

            def visit_unary_expression_node(self, node, parent_data):
                # Simple processing without generator
                return process_unary_expression(node)

    Usage:
        hlir = yaml_to_hlir(fragment.hlir)  # Convert YAML to HLIR
        visitor = MyVisitor()
        result = visitor.visit(hlir)

        # Example of visiting a specific node type:
        class CustomVisitor(Visitor):
            def visit_simple_type(self, node, parent_data):
                # Perform some operations on simple_type node
                return f"SimpleType: {node.name}"

            def visit_fn(self, node, parent_data):
                # Example with generator function
                print(f"Visiting function: {node.name}")
                function_data = yield f"Function {node.name}"
                print(f"Function {node.name} has children data: {function_data}")

            def __default__(self, node, parent_data):
                return node.__class__.__name__

        hlir = yaml_to_hlir(fragment.hlir)
        custom_visitor = CustomVisitor()
        result = custom_visitor.visit(hlir)
    """

    def visit(self, node: HLIRNode) -> Any:
        """
        Visits an HLIRNode recursively, handling child node processing.

        This method serves as the entry point for visiting a node. It initiates the
        recursive traversal, handles the final data processing, and returns the result
        from the generator.

        Args:
            node: Root node to visit.

        Returns:
            The result of visiting the node, potentially transformed.
        """
        generator = self._visit(node)
        try:
            result = next(generator)
            while True:
                next(generator)
        except StopIteration:
            pass

        return result

    def _visit(self, node: HLIRNode, parent_data: Optional[Any] = None, breadcrump: tuple[HLIRNode, ...] = ()) -> Any:
        """
        Recursively visits an HLIRNode, handling child node processing.

        This internal method identifies the appropriate visit method for the given node,
        processes its children, and optionally transforms the node.

        Args:
            node: Node to visit.

        Yields:
            The result of visiting the node, potentially transformed.
        """

        children_nodes = self._get_children_nodes(node)

        method_name = self._camel_to_snake(node.__class__.__name__)
        method = getattr(self, method_name, self.__default__)
        visitor_gen = method(node, parent_data, self._transform_breadcrump(breadcrump))

        if inspect.isgenerator(visitor_gen):
            node_data = next(visitor_gen)
        else:
            node_data = visitor_gen

        children_generators = {
            child_name: self._children_generator(child, node_data, breadcrump + (node,))
            for child_name, child in children_nodes.items()
        }

        children_data = {child_name: self._next(child_gen) for child_name, child_gen in children_generators.items()}

        final_data = None
        if inspect.isgenerator(visitor_gen):
            try:
                final_data = visitor_gen.send(children_data)
            except StopIteration:
                pass
        else:
            final_data = visitor_gen

        yield final_data

    def __default__(self, node: HLIRNode, children_data: Any, breadcrump: Any) -> Any:
        """
        The default method called if no specific visitor method exists for a node type.

        This method can be overridden in subclasses to provide default behavior for unhandled node types.

        Args:
           node: The node being visited.
           children_data: The data of the node's children.

        Returns:
           The node itself, typically unchanged.
        """
        return node

    def _transform_breadcrump(self, breadcrump: tuple[HLIRNode, ...]) -> Any:
        return breadcrump

    def _get_children_nodes(self, node: HLIRNode) -> Dict[str, Any]:
        """
        Retrieves the children of a given HLIRNode.

        This method collects all child nodes of the given node, ignoring private attributes.

        Args:
            node: The node whose children are to be retrieved.

        Returns:
            A dictionary mapping field names to their corresponding child nodes, tuples of child nodes, or other field
            values.
        """
        children = {}
        for field in fields(node):
            if field.name.startswith("_"):
                continue
            child = getattr(node, field.name)
            children[field.name] = child
        return children

    def _children_generator(self, child: Any, parent_data, breadcrump: tuple[HLIRNode, ...]) -> Any:
        """
        Creates a generator for visiting a child node or processing a tuple of child nodes.

        This method handles recursion for each child node appropriately. Tuples containing `HLIRNode`
        instances are processed recursively, while other values are returned unchanged.

        Args:
            child: The child node, tuple of child nodes, or other value to visit or process.

        Returns:
            A generator for the visited child node, a tuple of visited child nodes, or the unchanged value.
        """
        if isinstance(child, HLIRNode):
            return self._visit(child, parent_data, breadcrump)
        elif isinstance(child, tuple):
            # Only process tuples containing HLIRNodes
            if any(isinstance(c, HLIRNode) for c in child):
                return tuple(self._visit(c, parent_data, breadcrump) if isinstance(c, HLIRNode) else c for c in child)
            else:
                return child
        else:
            return child

    def _next(self, child_gen):
        """
        Advances the generator to the next yield point or retrieves the value for tuples and other types.

        Args:
            child_gen: The generator or value to advance or process.

        Returns:
            The next yielded value from the generator, a tuple of values, or the original value.
        """
        if inspect.isgenerator(child_gen):
            return next(child_gen)
        elif isinstance(child_gen, tuple):
            return tuple(self._next(item) for item in child_gen)
        else:
            return child_gen

    @staticmethod
    def _camel_to_snake(camel: str) -> str:
        """
        Converts a camelCase string to snake_case.

        Args:
            camel: The camelCase string to convert.

        Returns:
            The converted snake_case string.
        """
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel)
        ret = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

        if keyword.iskeyword(ret):
            ret = f"{ret}_"

        return ret
