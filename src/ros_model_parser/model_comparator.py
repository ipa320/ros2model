from pyparsing import *


def strip_slash(string):
    return '{}'.format(string[1:] if string.startswith('/') else string)

# find out missing and additional interfaces
# if both lists are empty, system is running fine
def compare_rossystem_models(model_ref, model_current):
    # not sure of the performance of this method
    set_ref = set((strip_slash(x.interface_name[0]))
                    for x in model_ref.interfaces)
    set_current = set((strip_slash(x.interface_name[0]))
                        for x in model_current.interfaces)

    # similarly for all interfaces within the node?
    # or only for topic connections?
    # does LED's code capture topic connections?
    ref_params = dict()
    for interface in model_ref.interfaces:
        for param in interface.parameters:
            key = strip_slash(param.param_name[0])
            ref_params[key] = [param.param_value[0],
                                interface.interface_name[0]]

    current_params = dict()
    for interface in model_current.interfaces:
        for param in interface.parameters:
            key = strip_slash(param.param_name[0])
            current_params[key] = [
                param.param_value[0], interface.interface_name[0]]

    incorrect_params = dict()
    for key, value in ref_params.items():
        try:
            current_value = current_params[key][0]
            ref_value = ref_params[key][0]

            if (type(current_value) is ParseResults) & (type(ref_value) is ParseResults):
                current_value = current_value.asList()
                ref_value = ref_value.asList()
            if (type(current_value) is str) & (type(ref_value) is str):
                current_value = re.sub(
                    r"[\n\t\s]*", "", strip_slash(current_value))
                ref_value = re.sub(
                    r"[\n\t\s]*", "", strip_slash(ref_value))
            isEqual = current_value == ref_value
            if not isEqual:
                incorrect_params.setdefault(current_params[key][1], [])
                incorrect_params[current_params[key]
                                    [1]].append([key, current_value])
        except Exception as exc:
            pass

    # returning missing_interfaces, additional_interfaces
    return list(set_ref - set_current), list(set_current - set_ref), incorrect_params

def _check_valid(interface_name, interface_type):
    if interface_type == '?':
        return False
    # add more cases here if required

    return True

def extract_common_ros(model_ref, model_current):
    node_ref = list(model_ref.packages[0].artifacts)[0].node
    node_current = list(model_current.packages[0].artifacts)[0].node

    set_ref_pub = set((strip_slash(pub.name[0]), pub.type[0]) for pub in node_ref.publishers if _check_valid(pub.name[0], pub.type[0]))
    set_current_pub = set((strip_slash(pub.name[0]), pub.type[0]) for pub in node_current.publishers if _check_valid(pub.name[0], pub.type[0]))

    set_ref_sub = set((strip_slash(sub.name[0]), sub.type[0]) for sub in node_ref.subscribers if _check_valid(sub.name[0], sub.type[0]))
    set_current_sub = set((strip_slash(sub.name[0]), sub.type[0]) for sub in node_current.subscribers if _check_valid(sub.name[0], sub.type[0]))

    set_ref_srv = set((strip_slash(srv.name[0]), srv.type[0]) for srv in node_ref.service_servers if _check_valid(srv.name[0], srv.type[0]))
    set_current_srv = set((strip_slash(srv.name[0]), srv.type[0]) for srv in node_current.service_servers if _check_valid(srv.name[0], srv.type[0]))

    set_ref_srv_cli = set((strip_slash(srv.name[0]), srv.type[0]) for srv in node_ref.service_clients if _check_valid(srv.name[0], srv.type[0]))
    set_current_srv_cli = set((strip_slash(srv.name[0]), srv.type[0]) for srv in node_current.service_clients if _check_valid(srv.name[0], srv.type[0]))

    set_ref_act = set((strip_slash(act.name[0]), act.type[0]) for act in node_ref.action_servers if _check_valid(act.name[0], act.type[0]))
    set_current_act = set((strip_slash(act.name[0]), act.type[0]) for act in node_current.action_servers if _check_valid(act.name[0], act.type[0]))

    set_ref_act_cli = set((strip_slash(act.name[0]), act.type[0]) for act in node_ref.action_clients if _check_valid(act.name[0], act.type[0]))
    set_current_act_cli = set((strip_slash(act.name[0]), act.type[0]) for act in node_current.action_clients if _check_valid(act.name[0], act.type[0]))

    return tuple(set_ref_pub.intersection(set_current_pub)), tuple(set_ref_sub.intersection(set_current_sub)), \
        tuple(set_ref_srv.intersection(set_current_srv)), tuple(set_ref_srv_cli.intersection(set_current_srv_cli)), \
        tuple(set_ref_act.intersection(set_current_act)), tuple(set_ref_act_cli.intersection(set_current_act_cli))
