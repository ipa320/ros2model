from typing import List, Optional

from pydantic import Field
from ros2model.api.runtime_parser.rosmodel_runtime_parser import (
    save_to_file,
    get_node_graph_names,
    parse,
)
import ros2model.core.metamodels.metamodel_ros as ROSModel
from pathlib import Path
from ros2model.core.utils import find_process_by_node_name


class RuntimeGraphName(ROSModel.GraphName):
    artifact_name: Optional[str] = None
    pkg_name: Optional[str] = None


class RuntimeNode(ROSModel.Node):
    name: RuntimeGraphName


class RuntimeRossystem(ROSModel.Rossystem):
    nodes: List[RuntimeNode] = Field(default_factory=list)

    def __init__(self, *, system: ROSModel.Rossystem, **data):
        super().__init__(name=system.name, **data)

    def get_nodes(self):
        nodes = get_node_graph_names()
        for n in nodes:
            pkg, artifact = find_process_by_node_name(n.name, n.namespace)

            parsed_node = parse(
                ROSModel.GraphName(
                    name=n.name,
                    namespace=n.namespace,
                    full_name=n.full_name,
                )
            )
            runtime_node = RuntimeNode(**parsed_node.model_dump())
            runtime_node.name.artifact_name = artifact
            runtime_node.name.pkg_name = pkg
            self.nodes.append(runtime_node)


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
