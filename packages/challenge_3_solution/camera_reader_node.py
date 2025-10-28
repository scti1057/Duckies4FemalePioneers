#!/usr/bin/env python3

import os
import rospy
import cv2
import yaml
import numpy as np
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
from std_msgs.msg import Float64


class CameraReaderNode(DTROS):
    def __init__(self, node_name):
        super(CameraReaderNode, self).__init__(node_name=node_name, node_type=NodeType.VISUALIZATION)

        self._vehicle_name = os.environ['VEHICLE_NAME']
        self._camera_topic = f"/{self._vehicle_name}/camera_node/image/compressed"
        self._bridge = CvBridge()
        self._window = "camera-reader"
        self._config_path = 'packages/challenge_3_solution/detect_lane.yaml'

        # Load configuration from YAML file
        with open(self._config_path, 'r') as f:
            self.conf = yaml.safe_load(f)

        self.target_x_buffer = []  # buffer to smooth target x values
        self.image = None

        # === Publisher ===
        self.pub_lane_x = rospy.Publisher(f"/{self._vehicle_name}/detect/lane_x", Float64, queue_size=1)

        # === Subscriber ===
        rospy.Subscriber(self._camera_topic, CompressedImage, self.image_callback, queue_size=1)

    # Converts ROS image message to OpenCV format
    def image_callback(self, msg):
        self.image = self._bridge.compressed_imgmsg_to_cv2(msg)

    # Create ROI polygon from config
    def create_polygon(self):
        return np.array([[
            [self.conf['lane_image']['top_left_x'], self.conf['lane_image']['top_left_y']],
            [self.conf['lane_image']['top_right_x'], self.conf['lane_image']['top_right_y']],
            [self.conf['lane_image']['bottom_right_x'], self.conf['lane_image']['bottom_right_y']],
            [self.conf['lane_image']['bottom_left_x'], self.conf['lane_image']['bottom_left_y']],
        ]], dtype=np.int32)

    # Calculate target x from detected contours inside the polygon mask
    def compute_target_x_from_polygon(self, polygon, mask_white, mask_yellow, image):
        min_area = 100

        # apply ROI polygon
        mask_poly = np.zeros_like(mask_white)
        cv2.fillPoly(mask_poly, polygon, 255)
        mw = cv2.bitwise_and(mask_white, mask_poly)
        my = cv2.bitwise_and(mask_yellow, mask_poly)

        # edge detection
        edges_white = cv2.Canny(cv2.GaussianBlur(mw, (5, 5), 0), 50, 150)
        edges_yellow = cv2.Canny(cv2.GaussianBlur(my, (5, 5), 0), 50, 150)

        # find contours
        contours_white, _ = cv2.findContours(edges_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_yellow, _ = cv2.findContours(edges_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # detect left (white) and right (yellow) boundaries
        left_x = None
        for cnt in contours_white:
            area = cv2.contourArea(cnt)
            if area <= min_area:
                continue
            M = cv2.moments(cnt)
            if M['m00'] == 0:
                continue
            cx = int(M['m10'] / M['m00'])
            if left_x is None or cx < left_x:
                left_x = cx
                cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)  # draw white lane contour

        right_x = None
        for cnt in contours_yellow:
            area = cv2.contourArea(cnt)
            if area <= min_area:
                continue
            M = cv2.moments(cnt)
            if M['m00'] == 0:
                continue
            cx = int(M['m10'] / M['m00'])
            if right_x is None or cx > right_x:
                right_x = cx
                cv2.drawContours(image, [cnt], -1, (0, 255, 255), 2)  # draw yellow lane contour

        ####
        'Challenge 3 solution: calculate target x'
        # compute midpoint
        if left_x is not None and right_x is not None and left_x > right_x:
            return ((left_x + right_x) / 2 - 30)
        elif right_x is not None:
            return right_x + 170
        elif left_x is not None:
            return left_x - 230
        else:
            return None
        'Challenge 3 solution end'
        ####

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if self.image is None:
                rate.sleep()
                continue

            image = self.image.copy()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # HSV ranges from config
            wh = self.conf['white']
            gh = self.conf['gelb']

            # make binary masks for white and yellow
            mask_white = cv2.inRange(hsv,
                                     (wh['hl'], wh['sl'], wh['vl']),
                                     (wh['hh'], wh['sh'], wh['vh']))
            mask_yellow = cv2.inRange(hsv,
                                      (gh['hl'], gh['sl'], gh['vl']),
                                      (gh['hh'], gh['sh'], gh['vh']))

            # morphological cleanup
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)
            mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_CLOSE, kernel)
            mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_OPEN, kernel)
            mask_yellow = cv2.morphologyEx(mask_yellow, cv2.MORPH_CLOSE, kernel)

            # Lane detection inside polygon
            polygon = self.create_polygon()
            target_x = self.compute_target_x_from_polygon(polygon, mask_white, mask_yellow, image)

            if target_x is not None:
                self.target_x_buffer.append(target_x)
                if len(self.target_x_buffer) > 2:
                    self.target_x_buffer.pop(0)

                smoothed_x = int(np.mean(self.target_x_buffer))
                target_y = image.shape[0] - 50


                ####
                'Challenge 3 solution: draw circle with text'
                # draw target
                #cv2.circle(img, center, radius, color, thickness)
                cv2.circle(image, (smoothed_x, target_y), 6, (255, 0, 255), -1)
                #cv2.putText(img, text, org, font, scale, color, thickness)
                cv2.putText(image, "Target", (smoothed_x - 20, target_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
                'Challenge 3 solution end'
                ####
                

                # publish target midpoint
                self.pub_lane_x.publish(Float64(smoothed_x))

            # Draw reference center of the image
            center_x = int(image.shape[1] / 2)
            center_y = image.shape[0] - 50
            cv2.circle(image, (center_x, center_y), 6, (0, 0, 255), -1)
            cv2.putText(image, "Center", (center_x - 25, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # Draw detection polygon
            cv2.polylines(image, polygon, isClosed=True, color=(255, 255, 255), thickness=2)

            # show debug window for visualization
            cv2.imshow(self._window, image)
            cv2.waitKey(1)

            rate.sleep()

    # keep config writeback
    def fnShutDown(self):
        with open(self._config_path, 'w') as f:
            yaml.dump(self.conf, f)
        print("Config saved")


if __name__ == '__main__':
    node = CameraReaderNode(node_name='camera_reader_node')
    node.run()
