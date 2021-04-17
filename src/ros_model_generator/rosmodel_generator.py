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

  def create_ros_model(self):
    ros_model_str = self.ros_model.dump_xtext_model()
    return True, ros_model_str

if __name__ == "__main__":
  generator = RosModelGenerator()
  try:
    print(generator.generate_ros_model("/tmp/test").dump())
  except Exception as e:
    print(e.args)
