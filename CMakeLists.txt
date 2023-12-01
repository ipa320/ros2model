cmake_minimum_required(VERSION 3.11)

project(ros_model_parser)

find_package(ament_cmake QUIET)

if(ament_cmake_FOUND)
  add_definitions(-DUSING_ROS2)
  message(STATUS "------------------------------------------")
  message(STATUS "pitasc_msgs is being built using AMENT.")
  message(STATUS "------------------------------------------")
  set(catkin_FOUND FALSE)

elseif(CATKIN_DEVEL_PREFIX OR CATKIN_BUILD_BINARY_PACKAGE)
  add_definitions(-DUSING_ROS)
  message(STATUS "------------------------------------------")
  message(STATUS "pitasc_msgs is being built using CATKIN.")
  message(STATUS "------------------------------------------")
  set(catkin_FOUND TRUE)
endif()

if(catkin_FOUND)
  find_package(catkin REQUIRED COMPONENTS
    rospy
  )

  catkin_python_setup()

  catkin_package()

  if(CATKIN_ENABLE_TESTING)
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
else()
  find_package(ament_cmake_python REQUIRED)
  find_package(rclpy REQUIRED)

  # Install Python modules
  ament_python_install_package(${PROJECT_NAME})

  # Install Python executables
  install(PROGRAMS
    scripts/parsers/ros_system_parser_example.py
    scripts/parsers/ros_parser_example.py
    scripts/generators/ros_model_generator_example.py
    scripts/generators/ros_system_model_generator_example.py
    scripts/generators/ros_system_model_generator_from_rosparamyaml_example.py
    DESTINATION lib/${PROJECT_NAME}
  )
endif()
