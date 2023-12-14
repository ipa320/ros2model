#!/usr/bin/env python
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


## ROS MODEL METAMODEL ##

from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List
from typing import Optional
import logging
import typing as t

GraphName = t.NewType("GraphName", str)


class Namespace(BaseModel):
    parts: List[GraphName] = Field(default_factory=list)


class QualityOfService(BaseModel):
    qoSProfile: str
    history: str
    depth: int
    reliability: str
    durability: str


class InterfaceType(BaseModel):
    namespace: Optional[Namespace] = None
    name: GraphName
    qos: Optional[QualityOfService] = None


class InterfaceTypeImpl(InterfaceType):
    type: str


class AbstrctType(BaseModel):
    pass


class string(AbstrctType):
    def value(self):
        return "string"


class bool(AbstrctType):
    def value(self):
        return "bool"


class int32(AbstrctType):
    def value(self):
        return "int32"


class uint32(AbstrctType):
    def value(self):
        return "uint32"


class float64(AbstrctType):
    def value(self):
        return "float64"


class float64Array(AbstrctType):
    def value(self):
        return "float64[]"


class int32Array(AbstrctType):
    def value(self):
        return "int32[]"


class SpecBase(BaseModel):
    name: str
    # package: Optional["Package"] = None
    # fullname: str | None = Field(None, validate_default=True)

    # @field_validator("fullname")
    # def set_if_empty(cls, v: str, info: ValidationInfo) -> str:
    #     v = info.data.get("name")
    #     return v


class MessagePart(BaseModel):
    type: str
    data: str


class MessageDefinition(BaseModel):
    messagePart: List[MessagePart] = list()


class TopicSpec(SpecBase):
    message: MessageDefinition


class TopicSpecMsgRef(AbstrctType):
    reference: TopicSpec


class ServiceSpec(SpecBase):
    request: Optional[MessageDefinition] = None
    response: Optional[MessageDefinition] = None


class ActionSpec(SpecBase):
    goal: MessageDefinition
    result: MessageDefinition
    feedback: Optional[MessageDefinition] = None


class Publisher(InterfaceTypeImpl):
    # message: TopicSpec
    pass


class Subscriber(InterfaceTypeImpl):
    # message: TopicSpec
    pass


class ServiceServer(InterfaceTypeImpl):
    # service: ServiceSpec
    pass


class ServiceClient(InterfaceTypeImpl):
    # service: ServiceSpec
    pass


class ActionServer(InterfaceTypeImpl):
    # action: ActionSpec
    pass


class ActionClient(InterfaceTypeImpl):
    # action: ActionSpec
    pass


class Dependency(BaseModel):
    pass


class Parameter(InterfaceType):
    pass


class Node(BaseModel):
    name: GraphName
    publisher: List[Publisher] = Field(default_factory=list)
    subscriber: List[Subscriber] = Field(default_factory=list)
    actionserver: List[ActionServer] = Field(default_factory=list)
    actionclient: List[ActionClient] = Field(default_factory=list)
    serviceserver: List[ServiceServer] = Field(default_factory=list)
    serviceclient: List[ServiceClient] = Field(default_factory=list)
    parameter: List[Parameter] = Field(default_factory=list)


class Artifact(BaseModel):
    name: str
    node: List[Node]


class Package(BaseModel):
    name: str
    spec: List[SpecBase] = Field(default_factory=list)
    artifact: List[Artifact] = Field(default_factory=list)
    fromGitRepo: Optional[str] = None
    dependency: List[Dependency] = Field(default_factory=list)

    def spec_defined(self) -> bool:
        return True if self.spec.count > 0 else False

    def get_topics(self):
        for spec in self.spec:
            if isinstance(spec, TopicSpec):
                yield spec

    def topics(self):
        return list(self.get_topics())

    def get_services(self):
        for spec in self.spec:
            if isinstance(spec, ServiceSpec):
                yield spec

    def services(self):
        return list(self.get_services())

    def get_actions(self):
        for spec in self.spec:
            if isinstance(spec, ActionSpec):
                yield spec

    def actions(self):
        return list(self.get_actions())


SpecBase.model_rebuild()


class CatkinPackage(Package):
    pass


class AmentPackage(Package):
    pass


# serialized = dump(builtin_interfaces.model_dump()).strip()
# print(serialized)
