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

        self.config = self._load_config()

        self._camera_topic = f"/{self._vehicle_name}/camera_node/image/compressed"
        self.bridge = CvBridge()
        self._vehicle_name = os.environ["VEHICLE_NAME"]

        self.sub_image = rospy.Subscriber(self._camera_topic, CompressedImage, self.cb_display_image, queue_size=1)
        rospy.loginfo(f"[{self.node_name}] Abonniert: {self._camera_topic}")

        self.Xth_frame = 1  # Verarbeite jedes X-te Frame


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
        if self.counter % self.Xth_frame != 0:
            self.counter += 1
            return
        else:
            self.counter += 1

        try:
            # ROS CompressedImage zu OpenCV-Bild
            np_arr = np.frombuffer(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
           
            window_name = f"{self._vehicle_name} Camera"
            # Beispieltext
            text = f"{self._vehicle_name} Girlsday HKA 2025"
            
        ####################################################
        # Aufgabe 2:                                       #
        # hier ToF Daten im Bild anzeigen lassen           #
        ####################################################

            # Text ins Bild einfügen (Position, Font, Größe, Farbe, Dicke)
            cv2.putText(
                cv_image,              # Bild
                text,                  # Textinhalt
                (20, 40),              # Position (x, y)
                cv2.FONT_HERSHEY_SIMPLEX,  # Schriftart
                1.0,                   # Schriftgröße
                (0, 255, 0),           # Farbe (BGR) -> Grün
                2,                     # Linienstärke
                cv2.LINE_AA            # Kantenglättung (Antialiasing)
            )
            cv2.imshow(window_name, cv_image)
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(window_name, 640, 480)
            cv2.waitKey(1)

        except Exception as e:
            rospy.logerr(f"[{self.node_name}] Fehler bei Bildverarbeitung: {e}")

    def on_shutdown(self):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    node = CameraNode(node_name="CameraNode")
    rospy.spin()
