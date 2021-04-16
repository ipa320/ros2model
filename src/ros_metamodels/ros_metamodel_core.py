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

## ROS MODEL METAMODEL ##
class Node(object):
    def __init__(self, name):
        self.name = name
        self.action_clients = InterfaceSet()
        self.action_servers = InterfaceSet()
        self.publishers = InterfaceSet()
        self.subscribers = InterfaceSet()
        self.service_clients = InterfaceSet()
        self.service_servers = InterfaceSet()
        self.params = ParameterSet()

    def dump_xtext_model(self):
        ros_model_str = "    Artifact "+self.name+" {\n"
        ros_model_str += "      Node { name " + self.name
        ros_model_str += self.service_servers.dump_xtext_model(
            "        ", "ServiceServer", "service", "ServiceServers")
        ros_model_str += self.service_clients.dump_xtext_model(
            "        ", "ServiceClients", "service", "ServiceClients")
        ros_model_str += self.publishers.dump_xtext_model(
            "        ", "Publisher", "message", "Publishers")
        ros_model_str += self.subscribers.dump_xtext_model(
            "        ", "Subscriber", "message", "Subscribers")
        ros_model_str += self.action_servers.dump_xtext_model(
            "        ", "ActionServer", "action", "ActionServers")
        ros_model_str += self.action_clients.dump_xtext_model(
            "        ", "ActionClient", "action", "ActionClients")
        ros_model_str += self.params.dump_xtext_model(
            "        ", "Parameters", "Parameters")
        ros_model_str += "}},\n"
        return ros_model_str

class Interface(object):
    def __init__(self, name, itype, namespace=""):
        self.resolved = name
        self.namespace = namespace
        self.minimal = name[len(self.namespace)-1:]
        self.itype = itype

    def dump_xtext_model(self, indent, name_type, interface_type):
        return ("%s%s { name '%s' %s '%s'}") % (
            indent, name_type, self.resolved, interface_type, self.itype.replace("/", "."))

class Parameter(object):
    def __init__(self, name, value, itype, namespace=""):
        self.resolved = name
        self.namespace = namespace
        self.minimal = name[len(self.namespace)-1:]
        self.value = value
        self.itype = self.get_type(value)
        self.count = 0

    def __eq__(self, other):
        if self.value == other.value and self.resolved == other.resolved:
            return True
        else:
            return False

    def get_type(self, value):
        itype = type(value)
        itype = (str(itype)).replace("<type '", "").replace("'>", "")
        if itype == 'float':
            return 'Double'
        elif itype == 'bool':
            return 'Boolean'
        elif itype == 'int':
            return 'Integer'
        elif itype == 'str':
            return 'String'
        elif itype == 'list' or itype == 'dict':
            if ":" in str(value):
                return 'Struct'
            else:
                return 'List'
        else:
            return itype

    def set_value(self, value, indent):
        str_param_value = ""
        if self.itype == "String":
            str_param_value += "'"+self.value+"'"
        elif self.itype == "Boolean":
            str_param_value += str(self.value).lower()
        elif self.itype == "List":
            str_param_value += str(self.value).replace(
                "[", "{").replace("]", "}")
        elif self.itype == 'Struct':
            str_param_value += self.value_struct(self.value[0], indent+"  ")
        else:
            str_param_value += str(value)
        return str_param_value

    def get_dict(self):
        return {"Value": self.value, "Name": self.resolved,
                "Namespace": self.namespace, "Minimal": self.minimal}

    def dump_xtext_model(self, indent="", value=""):
        str_param = "%sParameter { name '%s' type %s " % (
            indent, self.resolved, self.itype)
        if self.itype == 'Struct':
            str_param += self.types_struct(self.value[0], indent)
            #str_param = str_param[:-2]
        if self.itype == 'List':
            str_param += self.form_list(self.value)
        str_param += "}"
        return str_param



class InterfaceSet(set):
    def get_list(self):
        return [x.get_dict() for x in self]

    def iteritems(self):
        return [(x.resolved, x.itype) for x in self]

    def iterkeys(self):
        return [x.resolved for x in self]

    def dump_xtext_model(self, indent="", name_type="", interface_type="", name_block=""):
        if len(self) == 0:
            return ""
        str_ = ("\n%s%s {\n") % (indent, name_block)
        for elem in self:
            str_ += elem.dump_xtext_model(indent+"  ", name_type, interface_type) + ",\n"
        str_ = str_[:-2]
        str_ += "}"
        return str_

class ParameterSet(set):
    def get_list(self):
        return [x.get_dict() for x in self]

    def iteritems(self):
        return [(x.resolved, x.itype) for x in self]

    def iterkeys(self):
        return [x.resolved for x in self]

    def dump_xtext_model(self, indent="", value="", name_block=""):
        if len(self) == 0:
            return ""
        str_ = ("\n%s%s {\n") % (indent, name_block)
        for elem in self:
            str_ += elem.dump_xtext_model(indent+"  ", value) + ",\n"
        str_ = str_[:-2]
        str_ += "}"
        return str_

