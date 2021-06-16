# Ros Model Parser


[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![ROS Build Status](https://www.travis-ci.com/ipa320/ros_model_parser.svg?branch=master)](https://www.travis-ci.com/github/ipa320/ros_model_parser)
[![Python Build Status](https://github.com/ipa320/ros_model_parser/actions/workflows/build.yaml/badge.svg)](https://github.com/ipa320/ros_model_parser/actions/workflows/build.yaml)


Technical Maintainer: [**ipa-nhg**](https://github.com/ipa-nhg/) (**Nadia Hammoudeh Garcia**, **Fraunhofer IPA**) - **nadia.hammoudeh.garcia@ipa.fraunhofer.de**

This Ros package holds python interpreters for the [ROS models](https://github.com/ipa320/ros-model/) created using the [SeRoNet toolchain](https://www.seronet-projekt.de/platform/tooling.html). These models (.ros and .rossystem extensions) can be used to describe ROS nodes, their interaction and the instantiation at runtime for further information please check the [ROS model tutorials](https://github.com/ipa320/ros-model/#tutorials).


In addition, the Toolchain offers automatic extractors of the models from the original ROS code, on one hand with [static code analyzers](https://github.com/ipa320/ros-model-cloud) (based on [HAROS](https://github.com/git-afsantos/haros)) and on the other hand with [introspectors at runtime](https://github.com/ipa320/ros_graph_parser/).

For the static code analysis we made available a web interface able to inspect code hosted on Git and get its model representation as feedback [http://ros-model.seronet-project.de/](http://ros-model.seronet-project.de/). 


To facilitate the use of the models parsers we included to this repository and example script for the both supported models:

- Ros model parser [scripts/parsers/ros_parser_example.py](scripts/parsers/ros_parser_example.py) 
- RosSystem model parser [scripts/parsers/ros_system_parser_example.py](scripts/parsers/ros_system_parser_example.py)
- Ros model generator [scripts/generators/ros_model_generator_example.py](scripts/generators/ros_model_generator_example.py) 
- RosSystem model parser [scripts/generators/ros_system_model_generator_example.py](scripts/generators/ros_system_model_generator_example.py)
