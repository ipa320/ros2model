from pathlib import Path
from typing import Iterable, List, Tuple

from rosidl_runtime_py import (
    get_action_interfaces,
    get_interface_packages,
    get_interface_path,
    get_message_interfaces,
    get_service_interfaces,
)
from rosidl_adapter.parser import (
    ActionSpecification,
    MessageSpecification,
    ServiceSpecification,
    parse_action_file,
    parse_message_file,
    parse_service_file,
)

import ros2model.core.metamodels.metamodel_ros as ROSModel
from ros2model.api.model_generator.message_generator import MessageGenerator
from ros2model.verb import VerbExtension


def _format_field_type(field_type) -> str:
    """
    Convert a parsed field type to the canonical ROS interface string.

    This ensures message references include the '/msg/' namespace while leaving
    primitive types and already-qualified types untouched.
    """

    type_repr = str(field_type)
    array_suffix = ""
    array_start = type_repr.find("[")
    if array_start != -1:
        array_suffix = "[]"
        type_repr = type_repr[:array_start]
    else:
        array_start = None
    pkg_name = getattr(field_type, "pkg_name", None)
    if not pkg_name:
        return type_repr + array_suffix

    if any(segment in type_repr for segment in ("/msg/", "/srv/", "/action/")):
        return type_repr + array_suffix

    try:
        package, name = type_repr.split("/", 1)
    except ValueError:
        return type_repr + array_suffix

    return f"{package}/msg/{name}{array_suffix}"


def _message_definition_from_spec(
    message_spec: MessageSpecification,
) -> ROSModel.MessageDefinition:
    parts = [
        ROSModel.MessagePart(type=_format_field_type(field.type), data=field.name)
        for field in message_spec.fields
    ]
    return ROSModel.MessageDefinition(messagePart=parts)


def _service_spec_from_spec(
    spec: ServiceSpecification,
) -> ROSModel.ServiceSpec:
    return ROSModel.ServiceSpec(
        name=spec.srv_name,
        request=_message_definition_from_spec(spec.request),
        response=_message_definition_from_spec(spec.response),
    )


def _action_spec_from_spec(spec: ActionSpecification) -> ROSModel.ActionSpec:
    return ROSModel.ActionSpec(
        name=spec.action_name,
        goal=_message_definition_from_spec(spec.goal),
        result=_message_definition_from_spec(spec.result),
        feedback=_message_definition_from_spec(spec.feedback),
    )


class MessageVerb(VerbExtension):
    """Generate .ros models describing ROS interfaces."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "-o",
            "--output-folder",
            default=".",
            required=False,
            help="Directory where the generated .ros files are stored.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Generate models for every package that declares ROS interfaces.",
        )
        parser.add_argument(
            "-p",
            "--package",
            dest="packages",
            action="append",
            default=[],
            help="Generate models only for the given package. "
            "May be passed multiple times.",
        )

    def _resolve_packages(
        self, *, generate_all: bool, packages: Iterable[str]
    ) -> List[str]:
        if generate_all:
            return sorted(get_interface_packages().keys())

        unique = sorted({pkg for pkg in packages if pkg})
        if not unique:
            raise RuntimeError(
                "No package provided. Use --all or supply at least one -p option."
            )
        return unique

    def _gather_interfaces(
        self, package: str
    ) -> Tuple[List[str], List[str], List[str]]:
        msg_map = get_message_interfaces([package])
        srv_map = get_service_interfaces([package])
        action_map = get_action_interfaces([package])
        return (
            sorted(msg_map.get(package, [])),
            sorted(srv_map.get(package, [])),
            sorted(action_map.get(package, [])),
        )

    def main(self, *, args):
        try:
            package_names = self._resolve_packages(
                generate_all=args.all, packages=args.packages
            )
        except RuntimeError as exc:
            print(str(exc))
            return 1

        output_dir = Path(args.output_folder)
        if not output_dir.is_absolute():
            output_dir = output_dir.resolve()

        output_dir.mkdir(parents=True, exist_ok=True)

        generator = MessageGenerator()
        status = 0

        for package_name in package_names:
            message_names, service_names, action_names = self._gather_interfaces(
                package_name
            )
            if not (message_names or service_names or action_names):
                continue

            specs: List[ROSModel.SpecBase] = []

            # Messages
            for interface in message_names:
                _, _, msg_name = interface.partition("/")
                if not msg_name:
                    continue
                interface_identifier = f"{package_name}/{interface}"
                try:
                    interface_path = get_interface_path(interface_identifier)
                    parsed = parse_message_file(package_name, interface_path)
                except (LookupError, OSError, ValueError) as exc:
                    print(f"[warn] Skipping {interface_identifier}: {exc}")
                    status = 2
                    continue

                specs.append(
                    ROSModel.TopicSpec(
                        name=msg_name,
                        message=_message_definition_from_spec(parsed),
                    )
                )

            # Services
            for interface in service_names:
                _, _, srv_name = interface.partition("/")
                if not srv_name:
                    continue
                interface_identifier = f"{package_name}/{interface}"
                try:
                    interface_path = get_interface_path(interface_identifier)
                    parsed = parse_service_file(package_name, interface_path)
                except (LookupError, OSError, ValueError) as exc:
                    print(f"[warn] Skipping {interface_identifier}: {exc}")
                    status = 2
                    continue

                specs.append(_service_spec_from_spec(parsed))

            # Actions
            for interface in action_names:
                _, _, action_name = interface.partition("/")
                if not action_name:
                    continue
                interface_identifier = f"{package_name}/{interface}"
                try:
                    interface_path = get_interface_path(interface_identifier)
                    parsed = parse_action_file(package_name, interface_path)
                except (LookupError, OSError, ValueError) as exc:
                    print(f"[warn] Skipping {interface_identifier}: {exc}")
                    status = 2
                    continue

                specs.append(_action_spec_from_spec(parsed))

            if not specs:
                continue

            ros_package = ROSModel.Package(name=package_name, spec=specs)
            generator.generate_a_package(
                rosmodel=ros_package, output_dir=str(output_dir)
            )
            print(f"[info] Generated {package_name}.ros")

        return status
