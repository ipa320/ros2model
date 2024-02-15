from pathlib import Path

from ros2model.core.utils import find_process_by_node_name

from ros2cli.node.strategy import add_arguments

from ros2model.verb import VerbExtension
from ros2model.api.model_generator.component_generator import ComponentGenerator
import ros2model.api.runtime_parser.rosmodel_runtime_parser as RuntimeParser
import ros2model.core.metamodels.metamodel_ros as ROSModel


class RuntimeNodeVerb(VerbExtension):
    """Create .ros2 for each node in a runtime system"""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)

        parser.add_argument(
            "-o",
            "--output_folder",
            default=".",
            required=False,
            help="The folder for storing the generated models.",
        )

        parser.add_argument(
            "--include_hidden_nodes",
            action="store_true",
            required=False,
            help="Consider hidden nodes.",
        )

        parser.add_argument(
            "--include_hidden_interfaces",
            action="store_true",
            required=False,
            help="Consider hidden topics, services or actions.",
        )

    def name_component_file(self, grapg_name: ROSModel.GraphName):
        n = grapg_name.name.replace("/", "_")
        if grapg_name.namespace == "/":
            return n
        else:
            file_name = f"{grapg_name.namespace[1:]}__{n}"
            return file_name

    def main(self, *, args):
        output_dir = Path(args.output_folder)
        if output_dir.is_absolute() != True:
            output_dir = output_dir.resolve()

        node_generator = ComponentGenerator()

        nodes = RuntimeParser.get_node_graph_names()
        for n in nodes:
            node_instance = RuntimeParser.parse(
                ROSModel.GraphName(
                    name=n.name, namespace=n.namespace, full_name=n.full_name
                ),
                args.include_hidden_nodes,
                args.include_hidden_interfaces,
            )
            package_name, artifact_name = find_process_by_node_name(n.name, n.namespace)
            runtime_pkg = ROSModel.Package(
                name=package_name,
                artifact=[ROSModel.Artifact(name=artifact_name, node=[node_instance])],
            )
            node_generator.generate_a_file(
                model=runtime_pkg,
                output_dir=output_dir,
                filename=self.name_component_file(node_instance.name),
            )
