from pathlib import Path

from ros2cli.node.strategy import add_arguments

from ros2model.verb import VerbExtension
from ros2model.api.model_generator.system_generator import SystemGenerator
import ros2model.api.runtime_parser.rossystem_runtime_parser as RuntimeParser
import ros2model.core.metamodels.metamodel_ros as ROSModel
from ament_index_python import get_package_share_directory


class RuntimeVerb(VerbExtension):
    """Create .rossystem for a runtime system"""

    def add_arguments(self, parser, cli_name):
        add_arguments(parser)

        parser.add_argument(
            "-o",
            "--output_file",
            default=".",
            required=False,
            help="The system model file path.",
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

    def get_template(self):
        template_folder_ros = Path(
            get_package_share_directory("ros2model") + "/templates"
        )
        return (
            Path(template_folder_ros / "runtime_rossystem.rossystem.j2")
            .absolute()
            .as_posix()
        )

    def main(self, *, args):
        output_file = Path(args.output_file)
        system_name = output_file.name
        if output_file.is_absolute() != True:
            output_file = output_file.resolve()

        print(self.get_template())
        generator = SystemGenerator(template_path=self.get_template())

        system = RuntimeParser.RuntimeRossystem(
            system=ROSModel.Rossystem(name=system_name)
        )
        system.get_nodes()

        generator.generate_a_file(
            model=system,
            output_dir=output_file.parent,
            filename=system_name,
        )
