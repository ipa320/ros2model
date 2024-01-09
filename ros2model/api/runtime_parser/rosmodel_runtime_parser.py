import ros2model.core.metamodels.metamodel_ros as ROSModel
from ros2model.core.metamodels.metamodel_ros import set_full_name
import ros2node.api as ROS2Node
from ros2cli.node.strategy import NodeStrategy

from pydantic import BaseModel
from pathlib import Path
from rclpy.topic_endpoint_info import TopicEndpointInfo
import rclpy
from collections import namedtuple

Topic_BlackList = ["/parameter_events", "/rosout"]
Service_BlackList = [
    "/describe_parameters",
    "/get_parameter_types",
    "/get_parameters",
    "/list_parameters",
    "/set_parameters",
    "/set_parameters_atomically",
]

TopicInfoVerbose = namedtuple("TopicInfoVerbose", ("full_name", "info"))


def get_interface_name(node_namespace: str, interface_name: str):
    """get interface relative name

    Args:
        node_namespace (str): _description_
        interface_name (str): _description_

    Returns:
        _type_: _description_
    """
    if node_namespace != "/":
        prefix = f"{node_namespace}/"
    else:
        prefix = node_namespace

    if interface_name.startswith(prefix):
        interface_name = interface_name[len(prefix) :]
    return interface_name


def parse_interface(
    node: ROSModel.Node,
    typee: str,
    topic_info: ROS2Node.TopicInfo,
):
    """

    Args:
        node (ROSModel.Node): Node metamodel
        typee (str): the name of attribute in ROSModel.Node, e.g. publisher
        value (list[ROS2Node.TopicInfo]): TopicInfo = namedtuple('Topic', ('name', 'types'))

    """

    print(
        "parse_interface: interface_name:",
        get_interface_name(node.name.namespace, topic_info.name),
    )
    interface_name = get_interface_name(node.name.namespace, topic_info.name)

    interface = ROSModel.InterfaceTypeImpl(
        namespace=node.name.namespace,
        name=interface_name,
        type=topic_info.types[0],
    )
    # print("get interface:", interface)
    getattr(node, typee).append(interface)


def parse_interface_verbose(
    node: ROSModel.Node, typee: str, topic_endpoint_info: TopicInfoVerbose
):
    if topic_endpoint_info.full_name not in Topic_BlackList:
        print(f"topic name again: {topic_endpoint_info.full_name}\n")
        interface = ROSModel.InterfaceTypeImpl(
            namespace=node.name.namespace,
            name=topic_endpoint_info.full_name[len(node.name.namespace) :],
            type=topic_endpoint_info.info.topic_type,
            qos=ROSModel.QualityOfService(
                deadline=topic_endpoint_info.info.qos_profile.deadline.nanoseconds,
                reliability=topic_endpoint_info.info.qos_profile.reliability.name,
                history=topic_endpoint_info.info.qos_profile.history.name,
                durability=topic_endpoint_info.info.qos_profile.durability.name,
                liveliness=topic_endpoint_info.info.qos_profile.liveliness.name,
                liveliness_lease_duration=topic_endpoint_info.info.qos_profile.liveliness_lease_duration.nanoseconds,
            ),
        )
        print("get interface verbose: \n", interface)
        getattr(node, typee).append(interface)


class NodeArgs(BaseModel):
    node_name: str
    include_hidden_nodes: bool = False
    verbose: bool = False


class RunTimeNode(ROSModel.Node):
    pass

    def __init__(self, *, node: ROSModel.Node, **data):
        super().__init__(name=node.name, **data)

    class Config:
        arbitrary_types_allowed = True

    def get_publishers(self, node, include_hidden=False):
        try:
            topic_list = ROS2Node.get_publisher_info(
                node=node,
                remote_node_name=self.name.full_name,
                include_hidden=include_hidden,
            )
            for topicinfo in topic_list:
                if topicinfo.name not in Topic_BlackList:
                    infoall = node.get_publishers_info_by_topic(topicinfo.name)
                    for info in infoall:
                        nodename_from_topic = set_full_name(
                            info.node_namespace, info.node_name
                        )
                        if nodename_from_topic == self.name.full_name:
                            info_verbose = TopicInfoVerbose(
                                full_name=topicinfo.name, info=info
                            )
                            print(f"topic name: {info_verbose.full_name}\n")
                            parse_interface_verbose(self, "publisher", info_verbose)
                        else:
                            pass

        except AttributeError:
            pass

    def get_subscribers(self, node, include_hidden=False):
        try:
            topic_list = ROS2Node.get_subscriber_info(
                node=node,
                remote_node_name=self.name.full_name,
                include_hidden=include_hidden,
            )

            for topicinfo in topic_list:
                print(topicinfo.name)
                if topicinfo.name not in Topic_BlackList:
                    infoall = node.get_subscriptions_info_by_topic(topicinfo.name)
                    for info in infoall:
                        nodename_from_topic = set_full_name(
                            info.node_namespace, info.node_name
                        )
                        if nodename_from_topic == self.name.full_name:
                            info_verbose = TopicInfoVerbose(
                                full_name=topicinfo.name, info=info
                            )
                            parse_interface_verbose(self, "subscriber", info_verbose)
                        else:
                            pass

        except AttributeError:
            pass

    def get_service_servers(self, node, include_hidden=False):
        try:
            infos = ROS2Node.get_service_server_info(
                node=node,
                remote_node_name=self.name.full_name,
                include_hidden=include_hidden,
            )
            for info in infos:
                if (
                    info.name.startswith(self.name.full_name)
                    and info.name[len(self.name.full_name) :] in Service_BlackList
                ):
                    pass
                else:
                    parse_interface(self, "serviceserver", info)
        except AttributeError:
            pass

    def get_service_clients(self, node, include_hidden=False):
        try:
            info = ROS2Node.get_service_client_info(
                node=node,
                remote_node_name=self.name.full_name,
                include_hidden=include_hidden,
            )
            parse_interface(self, "serviceclient", info)
        except AttributeError:
            pass

    def get_action_servers(self, node, include_hidden=False):
        try:
            info_list = ROS2Node.get_action_server_info(
                node=node,
                remote_node_name=self.name.full_name,
                include_hidden=include_hidden,
            )
            for info in info_list:
                parse_interface(self, "actionserver", info)
        except AttributeError:
            pass

    def get_action_clients(self, node, include_hidden=False):
        try:
            info_list = ROS2Node.get_action_client_info(
                node=node,
                remote_node_name=self.name.full_name,
                include_hidden=include_hidden,
            )
            for info in info_list:
                parse_interface(self, "actionclient", info)
        except AttributeError:
            pass


def get_node_graph_names():
    args = NodeArgs(node_name="get_all_nodes")
    with NodeStrategy(args) as node:
        node_names = ROS2Node.get_node_names(
            node=node, include_hidden_nodes=args.include_hidden_nodes
        )
        return node_names


def parse(
    nodename: ROSModel.GraphName,
    include_hidden_nodes=False,
    include_hidden_interfaces=False,
):
    print(f"parse: node_name=get_{nodename.full_name}_info")
    args = NodeArgs(
        node_name=f"get_{nodename.full_name}_info",
        include_hidden_nodes=include_hidden_nodes,
        verbose=False,
    )
    with NodeStrategy(args) as node:
        parsed_node = RunTimeNode(node=ROSModel.Node(name=nodename))
        parsed_node.get_publishers(node, include_hidden=include_hidden_interfaces)
        parsed_node.get_subscribers(node, include_hidden=include_hidden_interfaces)
        parsed_node.get_service_servers(node, include_hidden=include_hidden_interfaces)
        parsed_node.get_service_clients(node, include_hidden=include_hidden_interfaces)
        parsed_node.get_action_clients(node, include_hidden=include_hidden_interfaces)
        parsed_node.get_action_servers(node, include_hidden=include_hidden_interfaces)
        return parsed_node


def save_to_file(result_path, full_name, instance):
    f_path = Path(str(result_path) + f"{full_name}.json")
    f_path.parent.mkdir(parents=True, exist_ok=True)
    with open(f_path, "w+") as f:
        f.write(instance.model_dump_json(indent=2))


def name_component_file(grapg_name: ROSModel.GraphName):
    n = grapg_name.name.replace("/", "_")
    file_name = f"{grapg_name.namespace}__{n}"
    return file_name


def main(result_path):
    nodes = get_node_graph_names()
    for n in nodes:
        print("node name: ", n.namespace, n.name, n.full_name)
        parsed_node = parse(
            ROSModel.GraphName(
                name=n.name, namespace=n.namespace, full_name=n.full_name
            )
        )
        save_to_file(
            result_path,
            name_component_file(n),
            parsed_node,
        )


if __name__ == "__main__":
    result_path = "./"
    main(result_path)
