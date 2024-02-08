from ros2model.api.runtime_parser.rosmodel_runtime_parser import (
    save_to_file,
    get_node_graph_names,
    parse,
)
import ros2model.core.metamodels.metamodel_ros as ROSModel
from pathlib import Path


class RuntimeRossystem(ROSModel.Rossystem):
    pass

    def __init__(self, *, system: ROSModel.Rossystem, **data):
        super().__init__(name=system.name, **data)

    def get_nodes(self):
        nodes = get_node_graph_names()
        for n in nodes:
            print("node name: ", n.namespace, n.name, n.full_name)
            parsed_node = parse(
                ROSModel.GraphName(
                    name=n.name, namespace=n.namespace, full_name=n.full_name
                )
            )
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
