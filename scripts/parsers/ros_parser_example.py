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

from ros_model_parser.rosmodel_parser import RosModelParser
from pyparsing import *
import os.path
import rospy
from rospkg import RosPack

def rossystem_parser_test():
    rp = RosPack()
    model_path = os.path.join(rp.get_path("ros_model_parser"),"resources/cob_light.ros")
    rossystem_parser = RosModelParser(model_path, isFile=True)

    static_model = rossystem_parser.parse()

    package = static_model.packages[0]
    for artifact in package.artifacts:
      node = artifact.node

      print "Package name: %s" %package.name
      print "Artifact name: %s" %artifact.name
      print "Node name: %s" %node.name
      if len(node.publishers) != 0:
          print "Publishers: "
          for pub in node.publishers:
              print"    Name: %s Type: %s" %(pub.name, pub.type)
      if len(node.subscribers) != 0:
          print "Subscribers: "
          for sub in node.subscribers:
              print"    Name: %s Type: %s" %(sub.name, sub.type)
      if len(node.service_servers) != 0:
          print "Service Servers: "
          for svr in node.service_servers:
              print"    Name: %s Type: %s" %(svr.name, svr.type)
      if len(node.service_clients) != 0:
          print "Service Clients: "
          for svr in node.service_clients:
              print"    Name: %s Type: %s" %(svr.name, svr.type)

if __name__ == '__main__':
    try:
        rossystem_parser_test()
    except rospy.ROSInterruptException:
        pass
