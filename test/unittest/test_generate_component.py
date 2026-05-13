import unittest
from pathlib import Path

from ros2model.api.model_generator.component_generator import ComponentGenerator
from ros2model.core.metamodels.metamodel_ros import *

test_model = Package(
    name="test_model",
    artifact=[
        Artifact(
            name="map_server",
            node=[
                Node(
                    name=GraphName(
                        name="map_server",
                        namespace="/",
                        full_name="/map_server",
                    ),
                    publisher=[
                        Publisher(name="map_metadata", type="nav_msgs/msg/MapMetaData"),
                        Publisher(name="map", type="nav_msgs/msg/OccupancyGrid"),
                    ],
                    serviceserver=[
                        ServiceServer(name="static_map", type="nav_msgs/srv/GetMap")
                    ],
                    serviceclient=[
                        ServiceClient(name="static_map", type="nav_msgs/srv/GetMap")
                    ],
                    actionclient=[
                        ActionClient(name="static_map", type="nav_msgs/srv/GetMap")
                    ],
                    actionserver=[
                        ActionServer(name="static_map", type="nav_msgs/srv/GetMap")
                    ],
                    parameter=[
                        Parameter(
                            name="shadows/min_angle", type="Double", value="-1.52"
                        )
                    ],
                ),
            ],
        ),
    ],
)

from devtools import pprint

# pprint(test_model)

test_dir = "test"
output_folder = Path(__file__).parent.parent / "outputs"

expect_result = """
test_model:
  artifacts:
    map_server:
      node: map_server
      publishers:
        'map_metadata':
          type: 'nav_msgs/msg/MapMetaData'
        'map':
          type: 'nav_msgs/msg/OccupancyGrid'
      actionservers:
        'static_map':
          type: 'nav_msgs/srv/GetMap'
      actionclients:
        'static_map':
          type: 'nav_msgs/srv/GetMap'
      serviceservers:
        'static_map':
          type: 'nav_msgs/srv/GetMap'
      serviceclients:
        'static_map':
          type: 'nav_msgs/srv/GetMap'
      parameters:
        'shadows/min_angle':
          type: Double
          value: -1.52

"""


class test_component_generator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = ComponentGenerator()
        self.test_dir = Path(test_dir)
        self.output_dir = Path(self.test_dir / output_folder)

    def test_generate_pkg(self):
        self.generator.generate_a_file(
            model=test_model,
            output_dir=self.output_dir,
            filename=f"{test_model.name}",
        )
        with open(Path(self.output_dir / f"{test_model.name}.ros2"), "r") as file:
            data = file.read()
        self.assertEqual(expect_result.strip(), data.strip())


class test_runtime_interface_names(unittest.TestCase):
    def test_namespaced_topic_is_made_relative(self):
        namespace, name = split_interface_name("/mavros", "/mavros/local_position/pose")

        self.assertEqual("/mavros", namespace)
        self.assertEqual("local_position/pose", name)
        self.assertEqual(
            "/mavros/local_position/pose",
            Publisher(
                namespace=namespace,
                name=name,
                type="geometry_msgs/msg/PoseStamped",
            ).full_name,
        )

    def test_namespace_without_leading_slash_is_normalized(self):
        self.assertEqual(
            ("/mavros", "local_position/pose"),
            split_interface_name("mavros", "/mavros/local_position/pose"),
        )

    def test_namespace_with_trailing_slash_is_normalized(self):
        self.assertEqual(
            ("/mavros/", "local_position/pose"),
            split_interface_name("/mavros/", "/mavros/local_position/pose"),
        )

    def test_global_topic_from_namespaced_node_stays_global(self):
        namespace, name = split_interface_name("/mavros", "/tf")

        self.assertEqual("/", namespace)
        self.assertEqual("tf", name)
        self.assertEqual(
            "/tf",
            Publisher(
                namespace=namespace,
                name=name,
                type="tf2_msgs/msg/TFMessage",
            ).full_name,
        )
        self.assertEqual(("/", "tf_static"), split_interface_name("/mavros", "/tf_static"))

    def test_root_namespace_topic_drops_leading_slash(self):
        self.assertEqual(("/", "diagnostics"), split_interface_name("/", "/diagnostics"))

    def test_relative_full_name_is_treated_as_root_topic(self):
        self.assertEqual(("/", "diagnostics"), split_interface_name("/mavros", "diagnostics"))

    def test_empty_full_name_is_preserved(self):
        self.assertEqual(("/mavros", ""), split_interface_name("/mavros", ""))
        self.assertEqual(("/", ""), split_interface_name("", ""))


if __name__ == "__main__":
    unittest.main()
