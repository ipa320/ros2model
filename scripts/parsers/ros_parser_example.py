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
import os.path

import rospy
from pyparsing import *
from rospkg import RosPack

from ros_model_parser.rosmodel_parser import RosModelParser


def ros_parser_test():
    rp = RosPack()
    model_path = os.path.join(
        rp.get_path("ros_model_parser"), "resources/cob_light.ros"
    )
    ros_parser = RosModelParser(model_path, isFile=True)

    static_model = ros_parser.parse()

    package = static_model.packages[0]
    for artifact in package.artifacts:
        node = artifact.node

        print("Package name: {0}".format(package.name))
        print("Artifact name: {0}".format(artifact.name))
        print("Node name: {0}".format(node.name))
        if len(node.publishers) != 0:
            print("Publishers: ")
            for pub in node.publishers:
                print("    Name: {0} Type: {1}".format(pub.name, pub.type))
        if len(node.subscribers) != 0:
            print("Subscribers: ")
            for sub in node.subscribers:
                print("    Name: {0} Type: {1}".format(sub.name, sub.type))
        if len(node.service_servers) != 0:
            print("Service Servers: ")
            for svr in node.service_servers:
                print("    Name: {0} Type: {1}".format(svr.name, svr.type))
        if len(node.service_clients) != 0:
            print("Service Clients: ")
            for svr in node.service_clients:
                print("    Name: {0} Type: {1}".format(svr.name, svr.type))
        if len(node.action_servers) != 0:
            print("Action Servers: ")
            for act in node.action_servers:
                print("    Name: {0} Type: {1}".format(act.name, act.type))
        if len(node.action_clients) != 0:
            print("Action Clients: ")
            for act in node.action_clients:
                print("    Name: {0} Type: {1}".format(act.name, act.type))


if __name__ == "__main__":
    try:
        ros_parser_test()
    except rospy.ROSInterruptException:
        pass
