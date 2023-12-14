cmake_minimum_required(VERSION 2.8.3)
project(ros_model_parser)

find_package(catkin REQUIRED COMPONENTS
    rospy
)

catkin_python_setup()

catkin_package()


if (CATKIN_ENABLE_TESTING)
  find_package(roslaunch REQUIRED)
  roslaunch_add_file_check(tests/model_generators_roslaunch_test.xml)
endif()

# INSTALL
catkin_install_python(PROGRAMS
  scripts/parsers/ros_system_parser_example.py
  scripts/parsers/ros_parser_example.py
  scripts/generators/ros_model_generator_example.py
  scripts/generators/ros_system_model_generator_example.py
  scripts/generators/ros_system_model_generator_from_rosparamyaml_example.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY resources tests
   DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
