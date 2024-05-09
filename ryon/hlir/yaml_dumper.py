import yaml
from ryon.hlir.nodes import HLIRNode


class YAMLHLIRDumper(yaml.Dumper):
    """Custom YAML dumper for handling HLIR."""

    pass


def hlir_node_representer(dumper: YAMLHLIRDumper, data: HLIRNode) -> yaml.nodes.MappingNode:
    return dumper.represent_mapping(f"!node.{data.__class__.__name__}", data.__dict__)


def hlir_tuple_representer(dumper: YAMLHLIRDumper, data: tuple) -> yaml.nodes.SequenceNode:
    return dumper.represent_list(data)


# Register custom representers to the custom YAML dumper
YAMLHLIRDumper.add_multi_representer(HLIRNode, hlir_node_representer)
YAMLHLIRDumper.add_representer(tuple, hlir_tuple_representer)


def hlir_to_yaml(node: HLIRNode) -> str:
    return yaml.dump(node, Dumper=YAMLHLIRDumper, indent=4, width=80, sort_keys=False)
