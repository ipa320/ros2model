import unittest
from pathlib import Path

from ros2model.api.model_generator.message_generator import MessageGenerator
from ros2model.core.metamodels.metamodel_ros import *

test_interfaces = Package(
    name="test_interfaces",
    spec=[
        TopicSpec(
            name="Duration",
            message=MessageDefinition(
                messagePart=[
                    MessagePart(type="int32", data="sec"),
                    MessagePart(type="int32", data="nanosec"),
                ]
            ),
        ),
        ServiceSpec(
            name="Trigger",
            response=MessageDefinition(
                messagePart=[
                    MessagePart(type="int32", data="success"),
                    MessagePart(type="int32", data="message"),
                ]
            ),
        ),
        ActionSpec(
            name="Fibonacci",
            goal=MessageDefinition(
                messagePart=[
                    MessagePart(type="int32", data="order"),
                ]
            ),
            result=MessageDefinition(
                messagePart=[
                    MessagePart(type="int32[]", data="sequence"),
                ]
            ),
            feedback=MessageDefinition(
                messagePart=[
                    MessagePart(type="int32[]", data="partial_sequence"),
                ]
            ),
        ),
    ],
)

test_dir = "test"
output_folder = "outputs"

expect_result = """
test_interfaces:
  msgs:
    Duration
        message
            int32 sec
            int32 nanosec
  srvs:
    Trigger
        request
        response
            int32 success
            int32 message
  actions:
    Fibonacci
        goal
            int32 order
        result
            int32[] sequence
        feedback
            int32[] partial_sequence

"""


class test_message_generator(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = MessageGenerator()
        self.test_dir = Path(test_dir)
        self.output_dir = Path(self.test_dir / output_folder)

    def test_generate_pkg(self):
        self.generator.generate_an_package(
            rosmodel=test_interfaces, output_dir=self.output_dir
        )
        with open(Path(self.output_dir / f"{test_interfaces.name}.ros"), "r") as file:
            data = file.read()
        self.assertEqual(expect_result.strip(), data.strip())


if __name__ == "__main__":
    unittest.main()
