import psutil
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterType


def find_process_by_node_name(node_name, namespace):
    for process in psutil.process_iter(["pid", "cmdline"]):
        try:
            cmdline = process.info["cmdline"]
            if namespace in str(cmdline) and node_name in str(cmdline):
                cmdline_list = cmdline[0].split("/")
                if len(cmdline_list) >= 3:
                    return cmdline_list[-2], cmdline_list[-1]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
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
