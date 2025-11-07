#!/usr/bin/env python3

import os

import numpy as np
import rospkg
import rospy
import yaml
import cv2
from cv_bridge import CvBridge
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import Bool, Float64, Int32, Int32MultiArray, String
from sensor_msgs.msg import CompressedImage, Range

class CameraNode(DTROS):
    def __init__(self, node_name):
        super(CameraNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        
        self._vehicle_name = os.environ["VEHICLE_NAME"]
        self._camera_topic = f"/{self._vehicle_name}/camera_node/image/compressed"
        self.bridge = CvBridge()


        self.sub_image = rospy.Subscriber(self._camera_topic, CompressedImage, self.cb_display_image, queue_size=1)
        rospy.loginfo(f"[{self.node_name}] Abonniert: {self._camera_topic}")

        self.counter = 0
        self.Xth_frame = 2  # Verarbeite jedes X-te Frame


        ####################################################
        # Aufgabe 2:                                       #
        # hier ToF Subscriber einfügen                     #
        ####################################################

        ####################################################
        # Aufgabe 2:                                       #
        # hier ToF Funktion einfügen                       #
        ####################################################

    def cb_display_image(self, image_msg):

        ########################################
        # Vorprogrammieren                     #
        ########################################
            
        ####################################################
        # Aufgabe 2:                                       #
        # hier ToF Daten im Bild anzeigen lassen           #
        ####################################################
        return

    def on_shutdown(self):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    node = CameraNode(node_name="CameraNode")
    rospy.spin()
