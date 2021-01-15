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

from ros_model_generator.rosmodel_generator import RosModelGenerator

import rospy


def ros_model_generator_test():

    ros_model = RosModelGenerator()
    ros_model.setPackageName("test_pkg")
    ros_model.setArtifactName("test_artifact")
    ros_model.setNodeName("test_node")
    ros_model.addPublisher("my_pub","std_msgs/Bool")
    ros_model.addParameter("myIntParam",25)

    ros_model.dump_java_ros_model("/tmp/test.ros")

if __name__ == '__main__':
    try:
        ros_model_generator_test()
    except rospy.ROSInterruptException:
        pass
