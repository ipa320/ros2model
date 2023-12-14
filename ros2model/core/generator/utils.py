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

from jinja2 import Environment, BaseLoader, TemplateNotFound, StrictUndefined
from pathlib import Path

import re

wordsplit = re.compile("([^_][^A-Z_]*)")


def camel_to_snake(string):
    return "_".join(s.lower() for s in wordsplit.findall(string))


def snake_to_camel(string):
    return "".join(s.capitalize() for s in wordsplit.findall(string))


class Loader(BaseLoader):
    def get_source(elf, environment, template):
        p = Path(template)
        if p.is_file():
            return p.read_text(), template, None
        raise TemplateNotFound(template)


def jinja_env():
    env = Environment(
        loader=Loader(),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        undefined=StrictUndefined,
    )
    env.filters["snake"] = camel_to_snake
    env.filters["camel"] = snake_to_camel
    return env
