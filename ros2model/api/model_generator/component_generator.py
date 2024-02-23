#
# Copyright 2023 Fraunhofer IPA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from pathlib import Path

from ros2model.core.generator.generator_core import GeneratorCore
import typing as t
import pkg_resources
import os

#Template_Folder = Path(__file__).parent.parent.parent.parent.resolve() / "templates"
Package_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(pkg_resources.resource_filename('ros2model', '')))))
Template_Folder = Path(os.path.join(os.path.join(os.path.join(Package_path,'share'),'ros2model'),'templates'))
Template = Path(Template_Folder / "component.ros2.j2")


try:
    from ament_index_python import get_package_share_directory

    Template_Folder_ROS = Path(get_package_share_directory("ros2model") + "/templates")
    Template_ROS = Path(Template_Folder_ROS / "component.ros2.j2")
except ImportError:
    Template_ROS = None


class ComponentGenerator(GeneratorCore):
    def __init__(self, template_path=None) -> None:
        if template_path != None:
            self.template_path = Path(template_path).resolve()
        elif Template_ROS != None and Template_ROS.is_file():
            self.template_path = Template
        elif Template.is_file():
            self.template_path = Template
        else:
            if Template_ROS != None:
                raise FileNotFoundError(
                    f"Can't find template either from {Template.absolute().as_posix()} or {Template_ROS.absolute().as_posix()}"
                )
            else:
                raise FileNotFoundError(
                    f"Can't find template either from {Template.absolute().as_posix()}"
                )
        super().__init__(self.template_path, ".ros2")
