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

import pprint
from pyparsing import *
import ros_model_generator.rosgraph_interface as model

class RosModelGenerator(object):
  def __init__(self):
    self.package_name= ""
    self.node_name = ""
    self.artifact_name = ""
    self.node=model.JavaNode(self.node_name)

  def setPackageName(self, name):
    self.package_name = name;
  def setArtifactName(self, name):
    self.artifact_name = name;
  def setNodeName(self, name):
    self.node_name = name;
    self.node.name = name;

  def addPublisher(self, name, topic_type):
    self.node.publishers.add(model.JavaInterface(name,topic_type))
  def addSubscriber(self, name, topic_type):
    self.node.subscribers.add(model.JavaInterface(name, topic_type))

  def addServiceServer(self, name, srv_type):
    self.node.service_servers.add(model.JavaInterface(name, srv_type))
  def addServiceClient(self, name, srv_type):
    self.node.service_clients.add(model.JavaInterface(name, srv_type))

  def addActionServer(self, name, act_type):
    self.node.action_servers.add(model.JavaInterface(name, act_type))
  def addActionClient(self, name, act_type):
    self.node.action_clients.add(model.JavaInterface(name, act_type))

  def addParameter(self, name, value):
    self.node.params.add(model.JavaParameterInterface(name, value, type(value)))

  def dump_java_ros_model(self, ros_model_file):
    sucess, ros_model_str = self.create_ros_model()
    with open(ros_model_file, 'w') as outfile:
      outfile.write(ros_model_str)

  def create_ros_model(self):
    ros_model_str = "PackageSet {\n"
    ros_model_str += "  CatkinPackage "+self.package_name + " { "
    ros_model_str += "\n"
    ros_model_str += self.node.dump_java_ros_model()
    ros_model_str = ros_model_str[:-2]
    ros_model_str += "\n}}"
    return True, ros_model_str


if __name__ == "__main__":
  generator = RosModelGenerator()
  try:
    print(generator.dump_java_ros_model("/tmp/test").dump())
  except Exception as e:
    print(e.args)

