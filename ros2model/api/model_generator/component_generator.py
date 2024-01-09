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
from ros2model.core.generator.file_generator import FileGenerator
import typing as t

Template_Folder = Path(__file__).parent.resolve() / "templates"
Template = Path(Template_Folder / "component.ros2.j2")


class ComponentGenerator(GeneratorCore):
    def __init__(self, template_path=None) -> None:
        if template_path != None:
            self.template_path = Path(template_path).resolve()
        else:
            self.template_path = Template
        super().__init__(self.template_path, ".ros2")
