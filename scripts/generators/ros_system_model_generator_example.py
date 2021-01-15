#!/usr/bin/env python
import imp

from ros_model_generator.rossystem_generator import RosSystemModelGenerator

import rospy


def ros_system_model_generator_test():
    ros_system_model = RosSystemModelGenerator()
    ros_system_model.setSystemName("test_system")
    ros_system_model.addParameter("mystring","test")
    ros_system_model.addParameter("myIntParam",25)

    ros_system_model.dump_java_ros_system_model("/tmp/test.rossystem")

if __name__ == '__main__':
    try:
        ros_system_model_generator_test()
    except rospy.ROSInterruptException:
        pass
