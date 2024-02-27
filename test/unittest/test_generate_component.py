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
output_folder = "outputs"

expect_result = """
test_model:
  artifacts:
    map_server:
      node: /map_server
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


if __name__ == "__main__":
    unittest.main()
