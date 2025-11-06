#!/usr/bin/env python3

import os

import time
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import Twist2DStamped
from std_msgs.msg import Float64, Int32, Int32MultiArray
from sensor_msgs.msg import Range


class ControlLaneNode(DTROS):
    def __init__(self, node_name):
        super(ControlLaneNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)

        self._vehicle_name = os.environ["VEHICLE_NAME"]


        # self.sub_ToF = rospy.Subscriber(f"/{self._vehicle_name}/front_center_tof_driver_node/range", Range, self.cb_ToF, queue_size=1)

        twist_topic = f"/{self._vehicle_name}/car_cmd_switch_node/cmd"
        self.pub_cmd_vel = rospy.Publisher(twist_topic, Twist2DStamped, queue_size=1)

        self.drive()
        rospy.on_shutdown(self.fnShutDown)

    ##############################################################
    # Aufgabe 3:                                                 #
    # Funktion zum Anhalten, wenn ein objekt zu nah ist Einfügen #
    ##############################################################


    def drive(self,v , omega, drive_time):
    ##########################################################################
    # Aufgabe 1:                                                             #
    # Funktion zum erstellen eines Fahr commandos                            #
    # Tipp: Zeiten verwenden um eine Gewisse Zeit in eine Richtung zu fahren #
    # Tipp: 2 Funktionen verwenden                                           #
    ##########################################################################
        return


    def fnShutDown(self):
        rospy.loginfo("Shutting down. cmd_vel will be 0")

        twist = Twist2DStamped(v=0.0, omega=0.0)
        self.pub_cmd_vel.publish(twist)


if __name__ == "__main__":
    # create the node
    node = ControlLaneNode(node_name="control_lane_node")
    # keep the process from terminating
    rospy.spin()
