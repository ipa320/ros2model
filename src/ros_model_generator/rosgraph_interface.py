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

from ros_graph_parser.core_class import *


class JavaInterface(Interface):
    def __init__(self, name, itype):
        super(JavaInterface, self).__init__(name, itype)

    def str_format(self, indent=""):
        return ("%sType: %s\n%sName: %s\n%sNamespace: %s\n%sMinimal: %s\n") % (
            indent, self.itype, indent, self.resolved, indent,
            self.namespace, indent, self.minimal)

    def java_format(self, indent="", name_type="", interface_type=""):
        return ("%s%s { name '%s' %s '%s'}") % (
            indent, name_type, self.resolved, interface_type, self.itype.replace("/", "."))


class JavaInterfaceSet(InterfaceSet):

    def str_format(self, indent=""):
        str_ = ""
        for elem in self:
            str_ += elem.str_format(indent) + "\n"
        return str_

    def java_format_ros_model(self, indent="", name_type="", interface_type="", name_block=""):
        if len(self) == 0:
            return ""
        str_ = ("\n%s%s {\n") % (indent, name_block)
        for elem in self:
            str_ += elem.java_format(indent+"  ",
                                     name_type, interface_type) + ",\n"
        str_ = str_[:-2]
        str_ += "}"
        return str_

    def java_format_system_model(self, indent="", name_type="", name_type2="", node_name="", pkg_name="", name_type3=""):
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


class JavaParameterInterface(ParameterInterface):
    def __init__(self, name, value, itype):
        super(JavaParameterInterface, self).__init__(name, value, itype)

    def str_format(self, indent=""):
        return ("%sType: %s\n%sName: %s\n%sNamespace: %s\n%sMinimal: %s\n") % (
            indent, self.value, indent, self.resolved, indent,
            self.namespace, indent, self.minimal)

    def java_format(self, indent="", value=""):
        str_param = "%sParameter { name '%s' type %s " % (
            indent, self.resolved, self.itype)
        if self.itype == 'Struct':
            str_param += self.types_struct(self.value[0], indent)
            #str_param = str_param[:-2]
        if self.itype == 'List':
            str_param += self.form_list(self.value)
        str_param += "}"
        return str_param


class JavaParameterSet(ParameterSet):

    def str_format(self, indent=""):
        str_ = ""
        for elem in self:
            str_ += elem.str_format(indent) + "\n"
        return str_

    def java_format_ros_model(self, indent="", value="", name_block=""):
        if len(self) == 0:
            return ""
        str_ = ("\n%s%s {\n") % (indent, name_block)
        for elem in self:
            str_ += elem.java_format(indent+"  ", value) + ",\n"
        str_ = str_[:-2]
        str_ += "}"
        return str_

    def java_format_system_model(self, indent="", name_type="", name_type2="", node_name="", pkg_name="", name_type3=""):
        if len(self) == 0:
            return ""
        if not name_type3:
            name_type3 = name_type2
        str_ = ("%sRos%s {\n") % (indent, name_type)
        for elem in self:
            str_ += ("%s    Ros%s '%s' {Ref%s '%s.%s.%s.%s' value %s},\n") % (
                indent, name_type3, elem.resolved, name_type2, pkg_name, node_name, node_name, elem.resolved, elem.set_value(elem.value, indent))
        str_ = str_[:-2]
        str_ += "}\n"
        return str_


class JavaNode(Node):
    def __init__(self, name=""):
        super(JavaNode, self).__init__(name="")

    def dump_java_ros_model(self):
        ros_model_str = "    Artifact "+self.name+" {\n"
        ros_model_str += "      Node { name " + self.name
        ros_model_str += self.service_servers.java_format_ros_model(
            "        ", "ServiceServer", "service", "ServiceServers")
        ros_model_str += self.service_clients.java_format_ros_model(
            "        ", "ServiceClients", "service", "ServiceClients")
        ros_model_str += self.publishers.java_format_ros_model(
            "        ", "Publisher", "message", "Publishers")
        ros_model_str += self.subscribers.java_format_ros_model(
            "        ", "Subscriber", "message", "Subscribers")
        ros_model_str += self.action_servers.java_format_ros_model(
            "        ", "ActionServer", "action", "ActionServers")
        ros_model_str += self.action_clients.java_format_ros_model(
            "        ", "ActionClient", "action", "ActionClients")
        ros_model_str += self.params.java_format_ros_model(
            "        ", "Parameters", "Parameters")
        ros_model_str += "}},\n"
        return ros_model_str

    def dump_java_system_model(self, package=""):
        system_model_str = "        ComponentInterface { name '" + \
            self.name+"'\n"
        system_model_str += self.publishers.java_format_system_model(
            "            ", "Publishers", "Publisher", self.name, package)
        system_model_str += self.subscribers.java_format_system_model(
            "            ", "Subscribers", "Subscriber", self.name, package)
        system_model_str += self.service_servers.java_format_system_model(
            "            ", "SrvServers", "Server", self.name, package, "ServiceServer")
        system_model_str += self.action_servers.java_format_system_model(
            "            ", "ActionServers", "ActionServer", self.name, package)
        system_model_str += self.action_clients.java_format_system_model(
            "            ", "ActionClients", "ActionClient", self.name, package)
        system_model_str += self.params.java_format_system_model(
            "            ", "Parameters", "Parameter", self.name, package)
        system_model_str += "},\n"
        return system_model_str
    
    def dump_print(self):
        _str = ""
        _str = "Node: \n\t%s" % (self.name)
        _str = _str + \
            "\tPublishers:\n%s" % (self.publishers.str_format('\t\t'))
        _str = _str + \
            "\tSubscribers:\n%s" % (self.subscribers.str_format('\t\t'))
        _str = _str + "\tServices:\n%s" % (self.service_servers.str_format('\t\t'))
        _str = _str + \
            "\tActionClients:\n%s" % (self.action_clients.str_format('\t\t'))
        _str = _str + \
            "\tActionServers:\n%s" % (self.action_servers.str_format('\t\t'))
        _str = _str + "\tParameters:\n%s" % (self.params.str_format('\t\t'))
        _str = _str + ("\n")
        print(_str)
