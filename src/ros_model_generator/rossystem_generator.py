#!/usr/bin/env python

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

