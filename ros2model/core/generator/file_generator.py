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
from .utils import jinja_env


# https://www.python.org/dev/peps/pep-0616/
def removesuffix(s, suffix):
    return s[: -len(suffix)] if s.endswith(suffix) else s


class FileGenerator:
    def __init__(self, output_folder: str):
        self.output_folder = Path(output_folder)
        self.generated = []
        self.env = jinja_env()

    def render_files(self, template_path, **data) -> str:
        template = self.env.get_template(str(Path(template_path).resolve()))
        return template.render(**data)

    def _add_generated(self, out):
        self.generated.append(out)

    def generate_file(self, template_path, file_name, **data):
        self.output_folder.mkdir(exist_ok=True, parents=True)
        out = self.output_folder / f"{file_name}"
        if out not in self.generated:
            self._add_generated(out)
            self.write_file(out, self.render_files(template_path, **data))

    def write_file(self, out, input):
        with open(out, "w", newline="") as f:
            f.write(input)
