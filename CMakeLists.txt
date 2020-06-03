cmake_minimum_required(VERSION 2.8.3)
project(ros_model_parser)

find_package(catkin REQUIRED COMPONENTS
    rospy
)

catkin_python_setup()

catkin_package()

# INSTALL
catkin_install_python(PROGRAMS scripts/rossystem_parser_example.py scripts/ros_parser_example.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY resources
   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
