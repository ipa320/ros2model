#!/usr/bin/env python
#
# Copyright 2020 Fraunhofer Institute for Manufacturing Engineering and Automation (IPA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import imp
import os

import rospkg
import rospy
import yaml

from ros_model_generator.rossystem_generator import RosSystemModelGenerator


def ros_system_model_generator_test():
    ros_system_model = RosSystemModelGenerator()
    ros_system_model.setSystemName("test_system")
    rospack = rospkg.RosPack()
    file_path = (
        rospack.get_path("ros_model_parser") + "/resources/rosparam_example.yaml"
    )
    for key, value in yaml.safe_load(open(os.path.join(file_path))).iteritems():
        ros_system_model.addParameter(key, value)

    ros_system_model.create_ros_system_model()

    ros_system_model.generate_ros_system_model("/tmp/test.rossystem")


if __name__ == "__main__":
    try:
        ros_system_model_generator_test()
    except rospy.ROSInterruptException:
        pass
