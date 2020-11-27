#!/usr/bin/env python
import imp

from ros_model_generator.rossystem_generator import RosSystemModelGenerator

import rospy
import yaml


def ros_system_model_generator_test():
    ros_system_model = RosSystemModelGenerator()
    ros_system_model.setSystemName("test_system")
    for key, value in yaml.load(open('../resources/rosparam_example.yaml')).iteritems():
        ros_system_model.addParameter(key,value)
    ros_system_model.dump_java_ros_system_model("/tmp/test")

if __name__ == '__main__':
    try:
        ros_system_model_generator_test()
    except rospy.ROSInterruptException:
        pass
