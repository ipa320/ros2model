#!/usr/bin/env python
#
# Copyright 2020 Fraunhofer Institute for Manufacturing Engineering and Automation (IPA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from ros_model_generator.rossystem_generator import RosSystemModelGenerator

import rospy


def ros_system_model_generator_test():
    ros_system_model = RosSystemModelGenerator()
    ros_system_model.setSystemName("test_system")
    ros_system_model.addParameter("mystring","test")
    ros_system_model.addParameter("myIntParam",25)

    ros_system_model.create_ros_system_model()

    ros_system_model.generate_ros_system_model('/tmp/test.rossystem')

def ros_system_model_generator_list_test():
    generator = RosSystemModelGenerator('demo', 'my_ros_package')
    components = {'/gazebo': {'parameters' : {'/gazebo/link_states' : [20, 'int']},
                              'publishers': {'/gazebo/link_states': 'gazebo_msgs/LinkStates',
                                             '/gazebo/model_states': 'gazebo_msgs/ModelStates'},
                              'subscribers': {'/gazebo/set_link_state': 'gazebo_msgs/LinkState',
                                              '/gazebo/set_model_state': 'gazebo_msgs/ModelState'},
                              'service_servers': {'/gazebo/spawn_sdf_model': 'gazebo_msgs/SpawnModel',
                                                  '/gazebo/spawn_urdf_model': 'gazebo_msgs/SpawnModel'}},
                 '/fibonacci': {'action_servers': {'/fibonacci': 'actionlib_tutorials/Fibonacci'}},
                                'global_parameters' : {'/gazebo/link_states' : [20, 'int']}}

    generator.generate_ros_system_model_list(components, '/tmp/test_list.rossystem', '/tmp/test_list.ros')


if __name__ == '__main__':
    try:
        ros_system_model_generator_test()
        ros_system_model_generator_list_test()
    except rospy.ROSInterruptException:
        pass
