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
import ros_metamodels.rossystem_metamodel_core as model

class RosSystemModelGenerator(object):
  def __init__(self,name=""):
    self.system = model.RosSystem(name);

  def setSystemName(self, name):
    self.system.name = name;

  def addParameter(self, name, value):
    self.system.params.add(model.Parameter(name, value, type(value)))

  def addComponent(self, name):
    self.system.components.add(model.Component(name))
  def addComponent(self, component):
    self.system.components.add(component)

  def dump_java_ros_system_model(self, rosystem_model_file):
    sucess, ros_system_model_str = self.create_ros_system_model()
    with open(rosystem_model_file, 'w') as outfile:
      outfile.write(ros_system_model_str)

  def create_ros_system_model(self):
    ros_system_model_str = self.system.dump_xtext_model()
    return True, ros_system_model_str

  def create_ros_system_model(self, node_names, pubs, subs, topics_dict, services_dict):
    for name in node_names:
      component = model.Component(name)
      for pub, node_name in pubs:
          # if not check_black_list(pub, BLACK_LIST_TOPIC):
          #     continue
          if name in node_name:
              # component.publishers.add(rg.Interface(pub, topics_dict[pub]))
              # component.publishers.add(model.RosInterface(pub, topics_dict[pub]))
              print(name)
              print(pub)
              print(node_name)
      # for sub, nodes_name in subs:
      #     if not check_black_list(sub, BLACK_LIST_TOPIC):
      #         continue
      #     if n in nodes_name:
      #         node.subscribers.add(rg.Interface(sub, topics_dict[sub]))
      # for serv, nodes_name in services:
      #     if not check_black_list(serv, BLACK_LIST_SERV):
      #         continue
      #     if n in nodes_name:
      #         node.services.add(rg.Interface(serv, services_dict[serv]))

      # node.check_actions()
      # nodes.append(node)

if __name__ == "__main__":
  generator = RosSystemModelGenerator()
  try:
    print(generator.dump_java_ros_system_model("/tmp/test").dump())
  except Exception as e:
    print(e.args)

