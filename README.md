# Ros Model Parser


[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![ROS Build Status](https://www.travis-ci.com/ipa320/ros2model.svg?branch=master)](https://www.travis-ci.com/github/ipa320/ros2model)
[![Python Build Status](https://github.com/ipa320/ros2model/actions/workflows/build.yaml/badge.svg)](https://github.com/ipa320/ros2model/actions/workflows/build.yaml)


Technical Maintainer: [**ipa-nhg**](https://github.com/ipa-nhg/) (**Nadia Hammoudeh Garcia**, **Fraunhofer IPA**) - **nadia.hammoudeh.garcia@ipa.fraunhofer.de**

This Ros package holds python interpreters for the [ROS models](https://github.com/ipa320/ros-model/) created using the [SeRoNet toolchain](https://www.seronet-projekt.de/platform/tooling.html). These models (.ros and .rossystem extensions) can be used to describe ROS nodes, their interaction and the instantiation at runtime for further information please check the [ROS model tutorials](https://github.com/ipa320/ros-model/#tutorials).


In addition, the Toolchain offers automatic extractors of the models from the original ROS code, on one hand with [static code analyzers](https://github.com/ipa320/ros-model-cloud) (based on [HAROS](https://github.com/git-afsantos/haros)) and on the other hand with [introspectors at runtime](https://github.com/ipa320/ros_graph_parser/).

For the static code analysis we made available a web interface able to inspect code hosted on Git and get its model representation as feedback [http://ros-model.seronet-project.de/](http://ros-model.seronet-project.de/).


## Install with ROS 2 (Humble or Rolling)
1. clone this repository into the source folder in your workspace, such as:
   ```
   ws/src/ros2model
   ```
2. Source ROS workspace

   Humble:
   ```
   source /opt/ros/humble/setup.bash
   ```

   Rolling:
   ```
   source /opt/ros/rolling/setup.bash
   ```
3. Back to the folder "ws", create and active venv
   ```
   python3 -m venv venv --system-site-packages --symlinks
   source venv/bin/activate
   ```
4. Install poetry and install dependencies
   run
   ```
   pip install poetry
   poetry install -C src/ros2model/
   ```
5. compile it as ROS package
   ```
   python -m colcon build --packages-select ros2model --symlink-install
   ```
   ```
   source install/local_setup.bash
   ```
6. config python path
   adjust the path to match the Python minor version in your virtual environment
   ```
   export PYTHONPATH=$PYTHONPATH:$(pwd)/venv/lib/$(python3 -c 'import sys; print(f"python{sys.version_info.major}.{sys.version_info.minor}")')/site-packages/
   ```

## Run
### Node models from a running system
Generate component models for each node discovered at runtime. Use `--include-description` if you need the `robot_description` parameter in the exported file and `--from-launch` to refine package/executable data with launch files.
```
ros2 model node -o test/nodes --include-description --from-launch my_pkg/bringup.launch.py
```
More options:
```
ros2 model node -h
```

### System model from a running system
Capture a full `.rossystem` model. The `--include-description` and `--from-launch` flags work the same way as for node models.
```
ros2 model system -o test/turtlesim.rossystem --include-description --from-launch turtlesim_gazebo/launch/sim_launch.py
```
More options:
```
ros2 model system -h
```

### Interface models from package definitions
Generate `.ros` models for topics, services, and actions declared in interface packages. Use `--all` to export every available package or pass `-p <package>` multiple times to target specific ones.
```
ros2 model msg --all -o test/interfaces
ros2 model msg -p std_msgs -p geometry_msgs -o test/interfaces
```
More options:
```
ros2 model msg -h
```
