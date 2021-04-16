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
import metamodel.metamodel_core as model

class RosSystemModelGenerator(object):
  def __init__(self,name=""):
    self.system = model.RosSystem(name);

  def setSystemName(self, name):
    self.system.name = name;

  def addParameter(self, name, value):
    self.system.params.add(model.Parameter(name, value, type(value)))

  def addComponent(self, name):
    self.system.components.add(model.Component(name))

  def dump_java_ros_system_model(self, rosystem_model_file):
    sucess, ros_system_model_str = self.create_ros_system_model()
    with open(rosystem_model_file, 'w') as outfile:
      outfile.write(ros_system_model_str)

  def create_ros_system_model(self):
    ros_system_model_str = self.system.dump_xtext_model()
    return True, ros_system_model_str


if __name__ == "__main__":
  generator = RosSystemModelGenerator()
  try:
    print(generator.dump_java_ros_system_model("/tmp/test").dump())
  except Exception as e:
    print(e.args)

