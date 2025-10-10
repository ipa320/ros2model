from typing import Dict, Tuple, Optional

from ros2model.api.runtime_parser.rosmodel_runtime_parser import (
    save_to_file,
    get_node_graph_names,
    parse,
)
import ros2model.core.metamodels.metamodel_ros as ROSModel
from pathlib import Path


from pydantic import Field


class RuntimeRossystem(ROSModel.Rossystem):
    include_hidden_nodes: bool = Field(default=False, exclude=True)
    include_hidden_interfaces: bool = Field(default=False, exclude=True)
    include_description: bool = Field(default=False, exclude=True)
    launch_mappings: Dict[str, Tuple[str, str]] = Field(
        default_factory=dict, exclude=True
    )

    def __init__(
        self,
        *,
        system: ROSModel.Rossystem,
        include_hidden_nodes: bool = False,
        include_hidden_interfaces: bool = False,
        include_description: bool = False,
        launch_mappings: Optional[Dict[str, Tuple[str, str]]] = None,
        **data,
    ):
        super().__init__(
            name=system.name,
            include_hidden_nodes=include_hidden_nodes,
            include_hidden_interfaces=include_hidden_interfaces,
            include_description=include_description,
            launch_mappings=launch_mappings or {},
            **data,
        )

    def _apply_launch_mapping(self, node: ROSModel.Node):
        if not self.launch_mappings:
            return
        candidate_keys = [
            getattr(node.name, "full_name", None),
            (
                getattr(node.name, "full_name", "").lstrip("/")
                if getattr(node.name, "full_name", None)
                else None
            ),
            getattr(node.name, "name", None),
        ]
        for key in candidate_keys:
            if not key:
                continue
            if key in self.launch_mappings:
                package, executable = self.launch_mappings[key]
                if hasattr(node, "package") and package:
                    if getattr(node, "package", None) in (None, "TODO"):
                        node.package = package
                if hasattr(node, "executable") and executable:
                    if getattr(node, "executable", None) in (None, "TODO"):
                        node.executable = executable
                break

    def get_nodes(self):
        nodes = get_node_graph_names()
        for n in nodes:
            print("node name: ", n.namespace, n.name, n.full_name)
            parsed_node = parse(
                ROSModel.GraphName(
                    name=n.name, namespace=n.namespace, full_name=n.full_name
                ),
                include_hidden_nodes=self.include_hidden_nodes,
                include_hidden_interfaces=self.include_hidden_interfaces,
            )
            if not self.include_description:
                filtered_parameters = [
                    param
                    for param in parsed_node.parameter
                    if param.name != "robot_description"
                ]
                parsed_node.parameter = filtered_parameters
            self._apply_launch_mapping(parsed_node)
            self.nodes.append(parsed_node)


def name_system_file(grapg_name: ROSModel.GraphName):
    n = grapg_name.name.replace("/", "_")
    file_name = f"{grapg_name.namespace}__{n}"
    return file_name


def main(result_file_path):
    system_name = Path(result_file_path).name
    system = RuntimeRossystem(system=ROSModel.Rossystem(name=system_name))
    system.get_nodes()
    save_to_file(
        result_path,
        system_name,
        system,
    )


if __name__ == "__main__":
    result_path = "./test.rossystem"
    main(result_path)
