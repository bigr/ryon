import yaml
from typing import Any
from ryon.hlir import nodes

from ryon.hlir.nodes import HLIRNode


class YAMLHLIRLoader(yaml.SafeLoader):
    """Custom YAML loader to deserialize HLIR."""


def hlir_node_constructor(loader: YAMLHLIRLoader, node_class_name, node: yaml.nodes.MappingNode) -> HLIRNode:
    fields: dict[str, Any] = loader.construct_mapping(node)
    cls = getattr(nodes, node_class_name)
    return cls(**fields)


def construct_yaml_tuple(loader: YAMLHLIRLoader, node: yaml.nodes.SequenceNode) -> tuple:
    init_list = loader.construct_sequence(node)
    return tuple(init_list)


# Register custom constructors to the loader
YAMLHLIRLoader.add_multi_constructor("!node.", hlir_node_constructor)
YAMLHLIRLoader.add_constructor("tag:yaml.org,2002:seq", construct_yaml_tuple)


def yaml_to_hlir(yaml_data: str) -> HLIRNode:
    return yaml.load(yaml_data, Loader=YAMLHLIRLoader)
