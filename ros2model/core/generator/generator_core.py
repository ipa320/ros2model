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

from ros2model.core.generator.file_generator import FileGenerator
from ros2model.core.exceptions import GeneratorError
import typing as t


class GeneratorCore:
    """
    Use jinja template to generate code
    """

    def __init__(self, template_path: t.Union[str, Path], extention: str) -> None:
        """
        Initialize GeneratorCore.

        Args:
            template_path (str or Path): the path of a template
            extention (str): the extention such as ".ros"

        Raises:
            GeneratorError: if can't find template or template doesn't have extention as ".j2"
        """
        self.template_path = Path(template_path).resolve()
        if self.template_path.is_file() == False:
            raise GeneratorError(f"{self.template_path} doesn't exist")
        if self.template_path.suffix != ".j2":
            raise GeneratorError(
                f"Please rename the extention of {self.template_path} to '.j2'"
            )
        self.ext = extention

    def generate_a_file(self, model: object, output_dir: t.Union[str, Path]):
        """
        Generate a file based on provided model and a template.
        Generated file will be named as the name of provided model

        Args:
            model (object): it will be used in template as object
            output_dir (str or Path): The folder storing a generated file
        """
        output_dir_path = Path(output_dir).resolve()
        generator = FileGenerator(output_dir_path)
        output_file_path = Path(output_dir_path / f"{model.name}{self.ext}")
        generator.generate_file(self.template_path, output_file_path, model=model)
