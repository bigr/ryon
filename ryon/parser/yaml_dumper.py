import yaml
from lark import Tree, Token


class YAMLASTDumper(yaml.Dumper):
    """Custom YAML dumper for handling Lark Tree and Token objects."""

    pass


def tree_representer(dumper: YAMLASTDumper, data: Tree) -> yaml.nodes.MappingNode:
    """
    Convert a Lark Tree object to a YAML mapping node.

    Args:
        dumper (YAMLASTDumper): The YAML dumper instance.
        data (Tree): The Lark Tree object to serialize.

    Returns:
        yaml.nodes.MappingNode: A YAML node representing the Tree.
    """
    if data.children:
        return dumper.represent_mapping("!Tree", {"node": data.data, "subtree": data.children})
    else:
        return dumper.represent_mapping("!Tree", {"node": data.data})


def token_representer(dumper: YAMLASTDumper, data: Token) -> yaml.nodes.ScalarNode:
    """
    Convert a Lark Token object to a YAML scalar node.

    Args:
        dumper (YAMLASTDumper): The YAML dumper instance.
        data (Token): The Lark Token object to serialize.

    Returns:
        yaml.nodes.ScalarNode: A YAML node representing the Token.
    """
    return dumper.represent_scalar("!Token", f"{data.type} {data.value}")


# Register custom representers to the custom YAML dumper
YAMLASTDumper.add_representer(Tree, tree_representer)
YAMLASTDumper.add_representer(Token, token_representer)


def ast_to_yaml(ast: Tree) -> str:
    """
    Serialize a Lark parse tree to a YAML formatted string using custom YAML dumper.

    Args:
        ast (Tree): The Lark parse tree to serialize.

    Returns:
        str: A YAML formatted string representing the parse tree.
    """
    return yaml.dump(ast, Dumper=YAMLASTDumper, indent=4, width=80)
