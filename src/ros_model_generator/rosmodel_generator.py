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
import ros_metamodels.ros_metamodel_core as model
import ros_metamodels.rossystem_metamodel_core as system_model

class RosModelGenerator(object):
  def __init__(self):
    self.ros_model = model.RosModel()

  def create_model_from_node(self, package_name, artifact_name, node):
      package = model.Package(package_name)
      artifact = model.Artifact(artifact_name, node)
      package.add_artifact(artifact)
      self.ros_model.add_package(package)

  def generate_ros_model(self, ros_model_file):
    sucess, ros_model_str = self.create_ros_model()
    with open(ros_model_file, 'w') as outfile:
      outfile.write(ros_model_str)

  def generate_ros_model_list(self, components, ros_model_file):
    sucess, ros_model_str = self.create_ros_model_list(components)
    with open(ros_model_file, 'w') as outfile:
      outfile.write(ros_model_str)

  def generate_ros_model_from_system(self, rossystem, package, ros_model_file, print_param_value=True):
    sucess, ros_model_str = self.create_ros_model_from_system(package, rossystem, print_param_value)
    with open(ros_model_file, 'w') as outfile:
      outfile.write(ros_model_str)

  def create_ros_model(self):
    ros_model_str = self.ros_model.dump_xtext_model()
    return True, ros_model_str

  def create_ros_model_from_system(self, package_name, rossystem, print_param_value=True):
    package = model.Package(package_name)
    for component in rossystem.components:
        node = model.Node(component.name)

        for param in component.params:
          node.add_parameter(param.resolved, None, None, param.value, print_param_value)

        for pub, pub_type in component.publishers.iteritems():
          node.add_publisher(pub, pub_type)

        for sub, sub_type in component.subscribers.iteritems():
          node.add_subscriber(sub, sub_type)

        for serv, serv_type in component.service_servers.iteritems():
          node.add_service_server(serv, serv_type)

        for serv, serv_type in component.service_clients.iteritems():
          node.add_service_client(serv, serv_type)

        for action, action_type in component.action_clients.iteritems():
          node.add_action_client(action, action_type)

        for action, action_type in component.action_servers.iteritems():
          node.add_action_server(action, action_type)

        artifact = model.Artifact(node.name, node)
        package.add_artifact(artifact)

    self.ros_model.add_package(package)
    return self.create_ros_model()

  def create_ros_model_list(self, components):
    for name in components:
      if name == 'global_parameters':
        continue
      node = model.Node(name)

      if 'parameters' in components[name]:
        parameters = components[name]['parameters']
        for param_name, param in parameters.items():
          node.add_parameter(param_name, None, None, param[0])

      if 'publishers' in components[name]:
        publishers = components[name]['publishers']
        for pub, pub_type in publishers.items():
          node.add_publisher(pub, pub_type)

      if 'subscribers' in components[name]:
        subscribers = components[name]['subscribers']
        for sub, sub_type in subscribers.items():
          node.add_subscriber(sub, sub_type)

      if 'service_servers' in components[name]:
        service_servers = components[name]['service_servers']
        for serv, serv_type in service_servers.items():
          node.add_service_server(serv, serv_type)

      if 'service_clients' in components[name]:
        service_clients = components[name]['service_clients']
        for serv, serv_type in service_clients.items():
          node.add_service_client(serv, serv_type)

      if 'action_clients' in components[name]:
        action_clients = components[name]['action_clients']
        for action, action_type in action_clients.items():
          node.add_action_client(action, action_type)

      if 'action_servers' in components[name]:
        action_servers = components[name]['action_servers']
        for action, action_type in action_servers.items():
          node.add_action_server(action, action_type)

      self.create_model_from_node('my_ros_pkg',"test",node)

    return self.create_ros_model()


if __name__ == "__main__":
  generator = RosModelGenerator()
  try:
    generator.generate_ros_model("/tmp/test")
  except Exception as e:
    print(e.args)
