#!/usr/bin/env python
import imp

from ros_model_parser.rosmodel_parser import RosModelParser
from pyparsing import *
import os.path
import rospy
from rospkg import RosPack

def rossystem_parser_test():
    rp = RosPack()
    model_path = os.path.join(rp.get_path("ros_model_parser"),"resources/cob_light.ros")
    rossystem_parser = RosModelParser(model_path, isFile=True)

    #rossystem_parser = RosModelParser("\
    #PackageSet { package { \
    #    CatkinPackage cob_light { artifact { \
    #        Artifact cob_light { \
    #            node Node { name cob_light_node"
    #,isFile=False)

    static_model = rossystem_parser.parse()

    package_name= static_model.get("pkg_name")
    node_name = static_model.get("node_name")
    publishers = static_model.get("publishers")
    subscribers = static_model.get("subscribers")
    svr_servers = static_model.get("svr_servers")
    svr_clients = static_model.get("svr_clients")

    print "Package name: %s" %package_name
    print "Node name: %s" %node_name
    if publishers is not None:
        print "Publishers: "
        for pub in publishers:
            print"    Name: %s Type: %s" %(pub.get("name"), pub.get("type"))
    if subscribers is not None:
        print "Subscribers: "
        for sub in subscribers:
            print"    Name: %s Type: %s" %(sub.get("name"), sub.get("type"))
    if svr_servers is not None:
        print "Service Servers: "
        for svr in svr_servers:
            print"    Name: %s Type: %s" %(svr.get("name"), svr.get("type"))
    if svr_clients is not None:
        print "Service Clients: "
        for svr in svr_clients:
            print"    Name: %s Type: %s" %(svr.get("name"), svr.get("type"))

if __name__ == '__main__':
    try:
        rossystem_parser_test()
    except rospy.ROSInterruptException:
        pass
