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

from distutils.core import setup

from setuptools import find_packages, setup

package_name = "ros2model"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/" + package_name, ["package.xml"]),
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (
            "share/" + package_name + "/templates",
            ["templates/component.ros2.j2", "templates/rossystem.rossystem.j2"],
        ),
    ],
    package_data={
        package_name: ['templates/*.j2'],
    },
    include_package_data=True,
    install_requires=[
        "jinja2",
        "pydantic",
        "pyaml",
        "lark",
        "devtools",
        "numpy",
        "netifaces",
    ],
    zip_safe=True,
    author="Nadia Hammoudeh Garcia, Ruichao Wu",
    author_email="nadia.hammoudeh.garcia@ipa.fraunhofer.de, ruichao.wu@ipa.fraunhofer.de",
    maintainer="Nadia Hammoudeh Garcia, Ruichao Wu",
    maintainer_email="nadia.hammoudeh.garcia@ipa.fraunhofer.de, ruichao.wu@ipa.fraunhofer.de",
    description="Parser for interface specifications",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "ros2cli.command": [
            "model = ros2model.command.model:ModelCommand",
        ],
        "ros2cli.extension_point": [
            "ros2model.verb = ros2model.verb:VerbExtension",
        ],
        "ros2model.verb": [
            "node = ros2model.verb.runtime_node:RuntimeNodeVerb",
            "system = ros2model.verb.runtime_system:RuntimeVerb",
        ],
    },
)
