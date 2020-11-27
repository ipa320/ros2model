#!/usr/bin/env python

import pprint
from pyparsing import *
import ros_graph_parser.core_class as systemmodel

class RosSystemModelGenerator(object):
  def __init__(self):
    self.system_name= ""

    self.system=systemmodel.Node(self.node_name)

  def setSystemName(self, name):
    self.system_name = name;

  def addNode(self, name, topic_type):
    self.node.publishers.add(model.Interface(name,topic_type))

  def addParameter(self, name, value):
    self.node.params.add(model.ParameterInterface(name, value, type(value)))

  def dump_java_ros_system_model(self, ros_model_file):
    sucess, ros_model_str = self.create_ros_model()
    with open(ros_model_file, 'w') as outfile:
      outfile.write(ros_model_str)

  def create_ros_system_model(self):
  ros_model_str = "PackageSet { package { \n"
  ros_model_str += "  CatkinPackage "+self.package_name + " { "
  ros_model_str += "artifact {\n"
  ros_model_str += self.node.dump_java_ros_model()
  ros_model_str = ros_model_str[:-2]
  ros_model_str += "\n}}}}"
  return True, ros_model_str


if __name__ == "__main__":
  generator = RosSystemModelGenerator()
  try:
    print(generator.dump_java_ros_system_model("/tmp/test").dump())
  except Exception as e:
    print(e.args)

