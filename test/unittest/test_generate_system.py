import unittest
from pathlib import Path

from ros2model.api.model_generator.system_generator import SystemGenerator
from ros2model.core.metamodels.metamodel_ros import *

test_model = Rossystem(
    name="test_system",
    nodes=[
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
            actionclient=[ActionClient(name="static_map", type="nav_msgs/srv/GetMap")],
            actionserver=[ActionServer(name="static_map", type="nav_msgs/srv/GetMap")],
            parameter=[
                Parameter(name="shadows/min_angle", type="Double", value="-1.52")
            ],
        ),
    ],
)

from devtools import pprint

pprint(test_model)

test_dir = "test"
output_folder = Path(__file__).parent.parent / "outputs"

expect_result = """
test_system:
  nodes:
    "/map_server":
      from: "/map_server"
      interfaces:
      	- "map_metadata": pub-> "TODO::map_metadata"
      	- "map": pub-> "TODO::map"
      	- "static_map": as-> "TODO::static_map"
      	- "static_map": ac-> "TODO::static_map"
      	- "static_map": ss-> "TODO::static_map"
      	- "static_map": sc-> "TODO::static_map"
      parameters:
        - shadows/min_angle: "/map_server.shadows/min_angle"
          value: -1.52

"""


class test_system_generator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = SystemGenerator()
        self.test_dir = Path(test_dir)
        self.output_dir = Path(self.test_dir / output_folder)

    def test_generate_pkg(self):
        self.generator.generate_a_file(
            model=test_model,
            output_dir=self.output_dir,
            filename=f"{test_model.name}",
        )
        with open(Path(self.output_dir / f"{test_model.name}.rossystem"), "r") as file:
            data = file.read()

        self.assertEqual(expect_result.strip(), data.strip())


if __name__ == "__main__":
    unittest.main()
