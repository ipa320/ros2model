#!/usr/bin/env python
import imp

from ros_model_generator.rosmodel_generator import RosModelGenerator

import rospy


def ros_model_generator_test():

    ros_model = RosModelGenerator()
    ros_model.setPackageName("test_pkg")
    ros_model.setArtifactName("test_artifact")
    ros_model.setNodeName("test_node")
    ros_model.addPublisher("my_pub","std_msgs/Bool")
    ros_model.addParameter("myIntParam",25)

    ros_model.dump_java_ros_model("/tmp/test")

if __name__ == '__main__':
    try:
        ros_model_generator_test()
    except rospy.ROSInterruptException:
        pass
