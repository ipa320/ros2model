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
import ros_graph_parser.core_class as model

class RosSystemModelGenerator(object):
  def __init__(self):
    self.system_name= ""
    self.parameters=list()

  def setSystemName(self, name):
    self.system_name = name;

  def addParameter(self, name, value):
    self.parameters.append(model.ParameterInterface(name, value, type(value)))

  def dump_java_ros_system_model(self, rosystem_model_file):
    sucess, ros_system_model_str = self.create_ros_system_model()
    with open(rosystem_model_file, 'w') as outfile:
      outfile.write(ros_system_model_str)

  def create_ros_system_model(self):
    ros_system_model_str = "RosSystem { Name '"+self.system_name+"' \n"
    if len(self.parameters)>0:
      ros_system_model_str+="  Parameters {\n"
      for param in self.parameters:
        ros_system_model_str += "   Parameter { name "+param.resolved+" type "+param.itype+" value "
        if param.itype=="String":
          ros_system_model_str +='"'+param.value+'"},\n'
        else:
          ros_system_model_str +=str(param.value)+"},\n"
      ros_system_model_str = ros_system_model_str[:-2]
      ros_system_model_str+="\n  }"
    ros_system_model_str += "\n}"
    return True, ros_system_model_str


if __name__ == "__main__":
  generator = RosSystemModelGenerator()
  try:
    print(generator.dump_java_ros_system_model("/tmp/test").dump())
  except Exception as e:
    print(e.args)

