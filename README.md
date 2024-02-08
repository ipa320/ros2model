# Ros Model Parser


[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![ROS Build Status](https://www.travis-ci.com/ipa320/ros2model.svg?branch=master)](https://www.travis-ci.com/github/ipa320/ros2model)
[![Python Build Status](https://github.com/ipa320/ros2model/actions/workflows/build.yaml/badge.svg)](https://github.com/ipa320/ros2model/actions/workflows/build.yaml)


Technical Maintainer: [**ipa-nhg**](https://github.com/ipa-nhg/) (**Nadia Hammoudeh Garcia**, **Fraunhofer IPA**) - **nadia.hammoudeh.garcia@ipa.fraunhofer.de**

This Ros package holds python interpreters for the [ROS models](https://github.com/ipa320/ros-model/) created using the [SeRoNet toolchain](https://www.seronet-projekt.de/platform/tooling.html). These models (.ros and .rossystem extensions) can be used to describe ROS nodes, their interaction and the instantiation at runtime for further information please check the [ROS model tutorials](https://github.com/ipa320/ros-model/#tutorials).


In addition, the Toolchain offers automatic extractors of the models from the original ROS code, on one hand with [static code analyzers](https://github.com/ipa320/ros-model-cloud) (based on [HAROS](https://github.com/git-afsantos/haros)) and on the other hand with [introspectors at runtime](https://github.com/ipa320/ros_graph_parser/).

For the static code analysis we made available a web interface able to inspect code hosted on Git and get its model representation as feedback [http://ros-model.seronet-project.de/](http://ros-model.seronet-project.de/).


## Install
1. clone this repository into the source folder in your workspace, such as:
    ```
    ws/src/ros2model
    ```
2. enter the folder "ws/src/ros2model"
   run
    ```
    ./install.sh
    ```

3. go back to "ws/":
    compile it as ros package
    ```
    colcon build --packages-up-to ros2model --symlink-install
    ```

## Run
1. Create ros node models from a run-time system:
    ```

    ros2 model node -o test/nodes # it will save generated file in folder "test/nodes"
    ```

    You can run the command below to get more usage information.
    ```
    ros2 model node -h
    ```

    ```
    usage: ros2 model node [-h] [--spin-time SPIN_TIME] [-s] [--no-daemon] [-o OUTPUT_FOLDER] [--include_hidden_nodes]
                        [--include_hidden_interfaces]

    Create .ros2 for each node in a runtime system

    options:
    -h, --help            show this help message and exit
    --spin-time SPIN_TIME
                            Spin time in seconds to wait for discovery (only applies when not using an already running daemon)
    -s, --use-sim-time    Enable ROS simulation time
    --no-daemon           Do not spawn nor use an already running daemon
    -o OUTPUT_FOLDER, --output_folder OUTPUT_FOLDER
                            The folder for storing the generated models.
    --include_hidden_nodes
                            Consider hidden nodes.
    --include_hidden_interfaces
                            Consider hidden topics, services or actions.
    ```

2. Create a ros system model from a run-time system:
    ```
    ros2 model system -o test/turtlesim # save the system in test folder and named as "turtlesim.rossystem"
    ```
    You can run the command below to get more usage information.
    ```
    ros2 model system -h
    ```
    ```
    usage: ros2 model system [-h] [--spin-time SPIN_TIME] [-s] [--no-daemon] [-o OUTPUT_FILE] [--include_hidden_nodes]
                         [--include_hidden_interfaces]

    Create .rossystem for a runtime system

    options:
    -h, --help            show this help message and exit
    --spin-time SPIN_TIME
                            Spin time in seconds to wait for discovery (only applies when not using an already running daemon)
    -s, --use-sim-time    Enable ROS simulation time
    --no-daemon           Do not spawn nor use an already running daemon
    -o OUTPUT_FILE, --output_file OUTPUT_FILE
                            The system model file path.
    --include_hidden_nodes
                            Consider hidden nodes.
    --include_hidden_interfaces
                            Consider hidden topics, services or actions.
    ```
