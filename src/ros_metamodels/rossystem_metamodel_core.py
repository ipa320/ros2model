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

from ros_metamodels.ros_metamodel_core import ParameterSet, Parameter

## ROS SYSTEM METAMODEL ##
class RosSystem(object):
    def __init__(self, name):
        self.name = name
        self.components = ComponentSet()
        self.params = ParameterSet()

    def dump_xtext_model(self):
        system_model_str = "RosSystem { Name '%s'\n" % self.name
        system_model_str += "    RosComponents ( \n"
        system_model_str += self.components.dump_xtext_model()
        system_model_str = system_model_str[:-2]
        system_model_str += "}\n)"
        system_model_str += self.params.dump_xtext_model(
            "        ", "Parameters", "Parameters")
        system_model_str += "}"

        return system_model_str


class Component(object):
    def __init__(self, name):
        self.name = name
        self.action_clients = RosInterfaceSet()
        self.action_servers = RosInterfaceSet()
        self.publishers = RosInterfaceSet()
        self.subscribers = RosInterfaceSet()
        self.service_clients = RosInterfaceSet()
        self.service_servers = RosInterfaceSet()
        self.params = RosParameterSet()

    def dump_xtext_model(self, package=""):
        system_model_str = "        ComponentInterface { name '" + \
            self.name+"'\n"
        system_model_str += self.publishers.dump_xtext_model(
            "            ", "Publishers", "Publisher", self.name, package)
        system_model_str += self.subscribers.dump_xtext_model(
            "            ", "Subscribers", "Subscriber", self.name, package)
        system_model_str += self.service_servers.dump_xtext_model(
            "            ", "SrvServers", "Server", self.name, package, "ServiceServer")
        system_model_str += self.action_servers.dump_xtext_model(
            "            ", "ActionServers", "Server", self.name, package)
        system_model_str += self.action_clients.dump_xtext_model(
            "            ", "ActionClients", "Client", self.name, package)
        system_model_str += self.params.dump_xtext_model(
            "            ", "Parameters", "Parameter", self.name, package)
        system_model_str += "        },\n"
        return system_model_str

class RosInterface(object):
    def __init__(self, name, reference, namespace=""):
        self.resolved = name
        self.namespace = namespace
        self.minimal = name[len(self.namespace)-1:]
        self.reference = reference

    def dump_xtext_model(self, indent, name_type, interface_type):
        return ("%s%s { name '%s' %s '%s'}") % (
            indent, name_type, self.resolved, interface_type, self.reference.replace("/", "."))

class ComponentSet(set):
    def get_list(self):
        return [x.get_dict() for x in self]

    def iteritems(self):
        return [(x.resolved, x.itype) for x in self]

    def iterkeys(self):
        return [x.resolved for x in self]

    def dump_xtext_model(self, indent="", value="", name_block=""):
        if len(self) == 0:
            return ""
        str_ = ("\n%s%s") % (indent, name_block)
        for elem in self:
            str_ += elem.dump_xtext_model() + "\n"
        str_ = str_[:-2]
        return str_

class RosInterfaceSet(set):
    def get_list(self):
        return [x.get_dict() for x in self]

    def iteritems(self):
        return [(x.resolved, x.reference) for x in self]

    def iterkeys(self):
        return [x.resolved for x in self]

    def dump_xtext_model(self, indent="", name_type="", name_type2="", node_name="", pkg_name="", name_type3=""):
        if len(self) == 0:
            return ""
        if not name_type3:
            name_type3 = name_type2
        str_ = ("%sRos%s {\n") % (indent, name_type)
        for elem in self:
            str_ += ("%s    Ros%s '%s' {Ref%s '%s.%s.%s.%s'},\n") % (
                indent, name_type3, elem.resolved, name_type2, pkg_name, node_name, node_name, elem.resolved)
        str_ = str_[:-2]
        str_ += "}\n"
        return str_

