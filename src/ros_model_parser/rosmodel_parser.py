#!/usr/bin/env python

import pprint
from pyparsing import *

# TODO: extract nodes, topics, services, etc from 'result'
# Compute Connections


# stateless functions
def parseActionStr(string, location, tokens):
    if((len(tokens[0]) == 1) and (type(tokens[0][0]) == str)):
        return tokens[0][0]


def parseActionDict(string, location, tokens):
    dict_list = list()
    for toks in tokens:
        param_dict = dict()
        for tok in toks:
            param_dict[tok[0]] = tok[1]
        dict_list.append(param_dict)
    return dict_list


class RosModelParser(object):
    def __init__(self, model, isFile=True):
        # OCB = Open Curly Bracket {}
        # CCB = Close Curly Bracket }
        # ORB = Open Round Bracket (
        # CRB = Close Round Bracket )
        # SQ = Single Quotes '
        # OSB = Open Square Bracket [
        # CSB = Close Square Bracket ]

        OCB, CCB, ORB, CRB, SQ, OSB, CSB = map(Suppress, "{}()'[]")
        name = Optional(SQ) + Word(printables,
                                   excludeChars="{},'") + Optional(SQ)

        real = Combine(Word(nums) + '.' + Word(nums))

        listStr = Forward()
        mapStr = Forward()
        param_value = Forward()

        sglQStr = QuotedString("'", multiline=True)
        string_value = Dict(
            Group(sglQStr + ZeroOrMore(OCB + param_value + CCB)))

        string_value.setParseAction(parseActionStr)
        values = (Combine(Optional("-") + real) | Combine(Optional("-") + Word(nums))).setParseAction(
            lambda tokens: float(tokens[0])) | string_value | Keyword("false") | Keyword("true") | listStr | mapStr

        _packageSet = Keyword("PackageSet").suppress()
        _package = Keyword("package").suppress()
        _catkin_pkg = Keyword("CatkinPackage").suppress()
        _artifact = Keyword("artifact").suppress()
        _artifacts = Keyword("Artifact").suppress()
        _node = Keyword("node").suppress()
        _nodes = Keyword("Node").suppress()
        _name = CaselessKeyword("name").suppress()

        # Types
        _srv_type= Keyword("service").suppress()
        _topic_type= Keyword("message").suppress()

        # Service Server
        _service_svrs= Keyword("serviceserver").suppress()
        _service_svr= Keyword("ServiceServer").suppress()
        service_svr = Group( _service_svr + OCB + _name + name("name") + _srv_type + name("type") + CCB)
        service_svrs = (_service_svrs + OCB + OneOrMore(service_svr + Optional(",").suppress()) + CCB)

        # Service Client
        _service_clis= Keyword("serviceclient").suppress()
        _service_cli= Keyword("ServiceClient").suppress()
        service_cli = Group( _service_cli + OCB + _name + name("name") + _srv_type + name("type") + CCB)
        service_clis = (_service_clis + OCB + OneOrMore(service_cli + Optional(",").suppress()) + CCB)

        # Publisher
        _pubs= Keyword("publisher").suppress()
        _pub= Keyword("Publisher").suppress()
        pub = Group( _pub + OCB + _name + name("name") + _topic_type + name("type") + CCB)
        pubs = (_pubs + OCB + OneOrMore(pub + Optional(",").suppress()) + CCB)

		# Subscriber
        _subs= Keyword("subscriber").suppress()
        _sub= Keyword("Subscriber").suppress()
        sub = Group( _sub + OCB + _name + name("name") + _topic_type + name("type") + CCB)
        subs = (_subs + OCB + OneOrMore(sub + Optional(",").suppress()) + CCB)

        self.rospkg_grammar = _packageSet + \
            OCB + \
            _package + OCB + \
            _catkin_pkg + name("pkg_name") + OCB + \
            _artifact + OCB + \
            _artifacts + name("artifact_name") + OCB + \
            _node + \
            _nodes + OCB + _name + name("node_name") + \
            Optional(service_svrs)("svr_servers") + \
            Optional(pubs)("publishers") + \
            Optional(subs)("subscribers") + \
            Optional(service_clis)("svr_clients")

        self._model = model
        self._isFile = isFile


    def _parse_from_string(self):
        self._result = self.rospkg_grammar.parseString(self._model)

    def _parse_from_file(self):
        self._result = self.rospkg_grammar.parseFile(self._model)

    def parse(self):
        self._result = ParseResults()
        try:
            if self._isFile:
                self._parse_from_file()
            else:
                self._parse_from_string()
        except Exception as e:
            print(e.args)   # Should set a default 'result'?
        return self._result


if __name__ == "__main__":
    import os
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(
        my_path, "../../resources/cob_light.ros")
    print(path)

    parser = RosModelParser(path)
    try:
        print(parser.parse().dump())
        # print(parser.parse().interfaces[2].services)
    except Exception as e:
        print(e.args)

