#!/usr/bin/env python
import imp

from ros_model_parser.rossystem_parser import RosSystemModelParser
from pyparsing import *
import os.path
import rospy
from rospkg import RosPack

def rossystem_parser_test():
    rp = RosPack()
    model_path = os.path.join(rp.get_path("ros_model_parser"),"resources/robotino.rossystem")
    rossystem_parser = RosSystemModelParser(model_path)
    static_model = rossystem_parser.parse()
    print(static_model);

if __name__ == '__main__':
    try:
        rossystem_parser_test()
    except rospy.ROSInterruptException:
        pass
