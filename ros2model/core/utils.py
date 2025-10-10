from pathlib import Path

import psutil
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterType


def find_process_by_node_name(node_name, namespace):
    """Best-effort lookup for the package/executable running a given node.

    This inspects the process table and matches processes whose ROS remap arguments
    or derived executable names align with the provided node name and namespace.
    """

    def extract_remaps(cmdline):
        remaps = {}
        for arg in cmdline:
            if not isinstance(arg, str):
                continue
            if arg.startswith("__node:="):
                remaps["__node"] = arg.split(":=", 1)[1]
            elif arg.startswith("__ns:="):
                value = arg.split(":=", 1)[1]
                remaps["__ns"] = value if value.startswith("/") else f"/{value}"
        return remaps

    def extract_package_exec_from_path(path_str):
        if not path_str or not isinstance(path_str, str):
            return None, None
        if "/lib/" not in path_str and "\\lib\\" not in path_str:
            return None, None
        try:
            path = Path(path_str)
        except (TypeError, ValueError):
            return None, None
        parts = path.parts
        for idx, part in enumerate(parts):
            if part == "lib" and idx + 2 < len(parts):
                package = parts[idx + 1]
                executable = parts[idx + 2]
                if executable:
                    return package, executable
        return None, path.name if path.name else None

    def extract_package_and_executable(cmdline, exe_path):
        for arg in cmdline:
            pkg, exe = extract_package_exec_from_path(arg)
            if pkg or exe:
                return pkg, exe
        pkg, exe = extract_package_exec_from_path(exe_path)
        if exe and exe.startswith("python"):
            exe = None
        return pkg, exe

    def possible_node_names(cmdline, exe_path):
        names = set()

        def add_candidate(value):
            if not value or not isinstance(value, str):
                return
            if value.startswith("-"):
                return
            names.add(Path(value).stem)

        if exe_path:
            add_candidate(exe_path)
        for arg in cmdline:
            if not isinstance(arg, str):
                continue
            if arg.startswith("__node:="):
                names.add(arg.split(":=", 1)[1])
                continue
            if arg.startswith("__ns:=") or arg in {"--ros-args", "--remap", "-r"}:
                continue
            add_candidate(arg)
        return {name for name in names if name}

    if not namespace:
        namespace = "/"
    elif namespace != "/" and not namespace.startswith("/"):
        namespace = f"/{namespace}"

    for process in psutil.process_iter(["pid", "cmdline", "exe"]):
        try:
            cmdline = process.info.get("cmdline") or []
            exe_path = process.info.get("exe")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

        if not cmdline:
            continue

        remaps = extract_remaps(cmdline)
        resolved_node = remaps.get("__node")
        resolved_ns = remaps.get("__ns")

        if resolved_node and resolved_node != node_name:
            continue

        if not resolved_ns:
            try:
                env_ns = process.environ().get("ROS_NAMESPACE")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                env_ns = None
            resolved_ns = env_ns if env_ns else "/"

        if resolved_ns != namespace:
            continue

        if not resolved_node:
            candidate_names = possible_node_names(cmdline, exe_path)
            if node_name not in candidate_names:
                continue

        package, executable = extract_package_and_executable(cmdline, exe_path)
        if package or executable:
            return package or "TODO", executable or "TODO"

    return "TODO", "TODO"


def get_param_value(pvalue: Parameter):
    if pvalue.type == ParameterType.PARAMETER_BOOL:
        label = "Boolean value is:"
        value = pvalue.bool_value
    elif pvalue.type == ParameterType.PARAMETER_INTEGER:
        label = "Integer value is:"
        value = pvalue.integer_value
    elif pvalue.type == ParameterType.PARAMETER_DOUBLE:
        label = "Double value is:"
        value = pvalue.double_value
    elif pvalue.type == ParameterType.PARAMETER_STRING:
        label = "String value is:"
        value = pvalue.string_value
    elif pvalue.type == ParameterType.PARAMETER_BYTE_ARRAY:
        label = "Byte values are:"
        value = pvalue.byte_array_value
    elif pvalue.type == ParameterType.PARAMETER_BOOL_ARRAY:
        label = "Boolean values are:"
        value = pvalue.bool_array_value
    elif pvalue.type == ParameterType.PARAMETER_INTEGER_ARRAY:
        label = "Integer values are:"
        value = pvalue.integer_array_value.tolist()
    elif pvalue.type == ParameterType.PARAMETER_DOUBLE_ARRAY:
        label = "Double values are:"
        value = pvalue.double_array_value.tolist()
    elif pvalue.type == ParameterType.PARAMETER_STRING_ARRAY:
        label = "String values are:"
        value = pvalue.string_array_value
    elif pvalue.type == ParameterType.PARAMETER_NOT_SET:
        label = "Parameter not set."
        value = None
    else:
        return f"Unknown parameter type '{pvalue.type}'"
    return value
