import ast
import os
from pathlib import Path
from typing import Dict, Optional, Tuple, List

from ament_index_python.packages import get_package_share_directory

from ros2cli.node.strategy import add_arguments

from ros2model.verb import VerbExtension
from ros2model.api.model_generator.system_generator import SystemGenerator
import ros2model.api.runtime_parser.rossystem_runtime_parser as RuntimeParser
import ros2model.core.metamodels.metamodel_ros as ROSModel


def _literal_eval_or_none(node):
    if node is None:
        return None
    try:
        return ast.literal_eval(node)
    except (ValueError, SyntaxError, TypeError):
        return None


def _call_name(call_node: ast.AST) -> str | None:
    if isinstance(call_node, ast.Name):
        return call_node.id
    if isinstance(call_node, ast.Attribute):
        return call_node.attr
    return None


def _build_full_name(namespace: str | None, name: str | None) -> str | None:
    if not name:
        return None
    if name.startswith("/"):
        return name
    if not namespace:
        return f"/{name}"
    ns = namespace if namespace.startswith("/") else f"/{namespace}"
    if ns != "/" and ns.endswith("/"):
        ns = ns.rstrip("/")
    return f"{ns}/{name}" if ns != "/" else f"/{name}"


def _eval_string(node: ast.AST, base_path: Path) -> Optional[str]:
    """Attempt to evaluate an AST node into a filesystem path string."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            else:
                return None
        return "".join(parts)
    if isinstance(node, ast.Call):
        func_name = _call_name(node.func)
        if func_name == "os.path.join":
            evaluated_parts: List[str] = []
            for arg in node.args:
                part = _eval_string(arg, base_path)
                if part is None:
                    return None
                evaluated_parts.append(part)
            return os.path.join(*evaluated_parts)
        if func_name == "get_package_share_directory":
            if not node.args:
                return None
            pkg_name = _literal_eval_or_none(node.args[0])
            if not isinstance(pkg_name, str):
                return None
            try:
                return get_package_share_directory(pkg_name)
            except LookupError:
                return None
        if func_name == "PythonLaunchDescriptionSource":
            if not node.args:
                return None
            return _eval_string(node.args[0], base_path)
    if isinstance(node, ast.List) and node.elts:
        evaluated = [_eval_string(elt, base_path) for elt in node.elts]
        if any(part is None for part in evaluated):
            return None
        return os.path.join(*evaluated)  # type: ignore[arg-type]
    return None


class _LaunchNodeExtractor(ast.NodeVisitor):
    def __init__(self, default_package: Optional[str], base_path: Path):
        self.default_package = default_package
        self.base_path = base_path
        self.mapping: Dict[str, Tuple[str, str]] = {}
        self.includes: List[Tuple[Path, Optional[str]]] = []

    def _record(self, key, package, executable):
        if not key or not package or not executable:
            return
        self.mapping.setdefault(key, (package, executable))

    def visit_Call(self, node):
        name = _call_name(node.func)
        if name == "Node":
            kwargs = {kw.arg: kw.value for kw in node.keywords if kw.arg}
            package = (
                _literal_eval_or_none(kwargs.get("package") or kwargs.get("pkg"))
                or self.default_package
            )
            executable = _literal_eval_or_none(
                kwargs.get("executable")
                or kwargs.get("node_executable")
                or kwargs.get("exec")
            )
            node_name = _literal_eval_or_none(
                kwargs.get("name") or kwargs.get("node_name")
            )
            namespace = _literal_eval_or_none(
                kwargs.get("namespace") or kwargs.get("ns")
            )
            full_name = _build_full_name(namespace, node_name)
            if full_name:
                self._record(full_name, package, executable)
            if node_name:
                self._record(node_name, package, executable)
        elif name == "IncludeLaunchDescription":
            candidate_nodes = list(node.args)
            candidate_nodes.extend(
                kw.value
                for kw in node.keywords
                if kw.arg == "launch_description_source"
            )
            for expr in candidate_nodes:
                path_str = _eval_string(expr, self.base_path)
                if not path_str:
                    continue
                candidate_path = Path(path_str)
                if not candidate_path.is_absolute():
                    candidate_path = (self.base_path / candidate_path).resolve()
                # try to infer package from get_package_share_directory if possible
                derived_pkg = self.default_package
                if isinstance(expr, ast.Call):
                    func_name = _call_name(expr.func)
                    if func_name == "PythonLaunchDescriptionSource" and expr.args:
                        inner = expr.args[0]
                        if (
                            isinstance(inner, ast.Call)
                            and _call_name(inner.func) == "os.path.join"
                        ):
                            for arg in inner.args:
                                if (
                                    isinstance(arg, ast.Call)
                                    and _call_name(arg.func)
                                    == "get_package_share_directory"
                                    and arg.args
                                ):
                                    pkg_candidate = _literal_eval_or_none(arg.args[0])
                                    if isinstance(pkg_candidate, str):
                                        derived_pkg = pkg_candidate
                self.includes.append((candidate_path, derived_pkg))
        self.generic_visit(node)


def _extract_nodes_from_launch(
    path: Path, default_package: Optional[str]
) -> Tuple[Dict[str, Tuple[str, str]], List[Tuple[Path, Optional[str]]]]:
    try:
        source = path.read_text()
    except OSError:
        print(f"[warn] Failed to read launch file '{path}'.")
        return {}, []
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        print(f"[warn] Could not parse launch file '{path}': {exc}")
        return {}, []
    visitor = _LaunchNodeExtractor(default_package, path.parent)
    visitor.visit(tree)
    return visitor.mapping, visitor.includes


def _collect_launch_mappings(entries) -> Dict[str, Tuple[str, str]]:
    mapping: Dict[str, Tuple[str, str]] = {}
    to_process: List[Tuple[Path, Optional[str]]] = []
    processed: set[Path] = set()
    for raw_entry in entries or []:
        if "/" not in raw_entry:
            print(
                f"[warn] Ignoring --from-launch entry '{raw_entry}'. "
                "Expected format 'package/relative_launch_file.py'."
            )
            continue
        package_name, relative_path = raw_entry.split("/", 1)
        try:
            share_dir = Path(get_package_share_directory(package_name))
        except LookupError:
            print(
                f"[warn] Package '{package_name}' from --from-launch entry '{raw_entry}' not found."
            )
            continue
        candidate = share_dir / "launch" / relative_path
        if not candidate.exists():
            candidate = share_dir / relative_path
        if not candidate.exists():
            print(
                f"[warn] Launch file '{relative_path}' not found in package '{package_name}'."
            )
            continue
        if candidate.suffix != ".py":
            print(f"[warn] Skipping non-Python launch file '{candidate}'.")
            continue
        to_process.append((candidate.resolve(), package_name))

    while to_process:
        path, pkg_hint = to_process.pop()
        if path in processed:
            continue
        processed.add(path)
        nodes, includes = _extract_nodes_from_launch(path, pkg_hint)
        for key, value in nodes.items():
            mapping.setdefault(key, value)
        for include_path, include_pkg in includes:
            if not include_path.exists():
                print(f"[warn] Included launch file '{include_path}' not found.")
                continue
            if include_path.suffix != ".py":
                continue
            to_process.append((include_path.resolve(), include_pkg or pkg_hint))
    return mapping


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
        parser.add_argument(
            "--include-description",
            action="store_true",
            required=False,
            help="Include robot_description parameters in the output.",
        )
        parser.add_argument(
            "--from-launch",
            nargs="+",
            default=[],
            metavar="PACKAGE/LAUNCH_FILE",
            help=(
                "Optionally parse one or more launch files to refine package/executable "
                "information (format: package/relative/path.py)."
            ),
        )

    def main(self, *, args):
        output_file = Path(args.output_file)
        system_name = output_file.name
        if output_file.is_absolute() != True:
            output_file = output_file.resolve()

        generator = SystemGenerator()
        launch_mapping = _collect_launch_mappings(args.from_launch)

        system = RuntimeParser.RuntimeRossystem(
            system=ROSModel.Rossystem(name=system_name),
            include_hidden_nodes=args.include_hidden_nodes,
            include_hidden_interfaces=args.include_hidden_interfaces,
            include_description=args.include_description,
            launch_mappings=launch_mapping,
        )
        system.get_nodes()

        generator.generate_a_file(
            model=system,
            output_dir=output_file.parent,
            filename=system_name,
        )
