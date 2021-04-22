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

  def dump_ros_system_model(self, rosystem_model_file):
    sucess, ros_system_model_str = self.create_ros_system_model()
    with open(rosystem_model_file, 'w') as outfile:
      outfile.write(ros_system_model_str)

  def dump_ros_system_model_list(self, components, rosystem_model_file):
    sucess, ros_system_model_str = self.create_ros_system_model_list(components)
    with open(rosystem_model_file, 'w') as outfile:
      outfile.write(ros_system_model_str)

  def create_ros_system_model(self):
    ros_system_model_str = self.system.dump_xtext_model()
    return True, ros_system_model_str

  def create_ros_system_model_list(self, components):
    for name in components:
      component = model.Component(name)

      if 'parameters' in components[name]:
        parameters = components[name]['parameters']
        for name, value in parameters.items():
          component.params.add(model.RosParameter(name, value))

      if 'publishers' in components[name]:
        publishers = components[name]['publishers']
        for pub, pub_type in publishers.items():
          component.publishers.add(model.RosInterface(pub, pub_type))

      if 'subscribers' in components[name]:
        subscribers = components[name]['subscribers']
        for sub, sub_type in subscribers.items():
          component.subscribers.add(model.RosInterface(sub, sub_type))

      if 'service_servers' in components[name]:
        service_servers = components[name]['service_servers']
        for serv, serv_type in service_servers.items():
          component.service_servers.add(model.RosInterface(serv, serv_type))

      if 'service_clients' in components[name]:
        service_clients = components[name]['service_clients']
        for serv, serv_type in service_clients.items():
          component.service_clients.add(model.RosInterface(serv, serv_type))

      if 'action_clients' in components[name]:
        action_clients = components[name]['action_clients']
        for action, action_type in action_clients.items():
          component.action_clients.add(model.RosInterface(action, action_type))

      if 'action_servers' in components[name]:
        action_servers = components[name]['action_servers']
        for action, action_type in action_servers.items():
          component.action_servers.add(model.RosInterface(action, action_type))

      self.addComponent(component)

    if 'parameters_node' in components:
      component = model.Component('parameters_node')
      parameters = components['parameters_node']['parameters']
      for name, value in parameters.items():
        component.params.add(model.RosParameter(name, value))
      self.addComponent(component)

    return self.create_ros_system_model()


if __name__ == "__main__":
  generator = RosSystemModelGenerator()
  components = {'/gazebo': {'publishers': {'/gazebo/link_states': 'gazebo_msgs/LinkStates',
                                           '/gazebo/model_states': 'gazebo_msgs/ModelStates'},
                            'subscribers': {'/gazebo/set_link_state': 'gazebo_msgs/LinkState',
                                            '/gazebo/set_model_state': 'gazebo_msgs/ModelState'},
                            'service_servers': {'/gazebo/spawn_sdf_model': 'gazebo_msgs/SpawnModel',
                                                '/gazebo/spawn_urdf_model': 'gazebo_msgs/SpawnModel'}},
              '/fibonacci': {'action_servers': {'/fibonacci': 'actionlib_tutorials/Fibonacci'}}}
  try:
    # print(generator.dump_ros_system_model("/tmp/test").dump())
    print(generator.create_ros_system_model_list(components)[1])
  except Exception as e:
    print(e.args)

