#!/usr/bin/env python
import rospy
import message_filters
import ros_numpy
import tf

from sensor_msgs.msg import Image, CameraInfo, PointCloud2

import numpy as np
import cv2

from cv_bridge import CvBridge

class ParseImageToRGB:

    def __init__(self, image_sub_topic, image_pub_topic):
        self.shown = False
        self.image_sub = rospy.Subscriber(image_sub_topic, Image, self.callback)
        self.rgb_image_pub = rospy.Publisher(image_pub_topic, Image)
        self.bridge = CvBridge()

    def show_image(self, img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(3)

    def callback(self, data):
        rgb_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        if not self.shown:
            self.show_image(rgb_image)
            # cv2.imshow('kinect_rgb_image', rgb_image)
            # self.rgb_image_pub.publish(data)
            print(rgb_image.shape)
            self.shown = True


def main():
    # This image does not have color 
    RGB_IMAGE_TOPIC = '/camera/rgb/image_raw'
    RGB_REAL_IMAGE_TOPIC = '/kinect_rgb_image'

    rospy.init_node('kinect_rgb_image_transform')
    ParseImageToRGB(RGB_IMAGE_TOPIC, RGB_REAL_IMAGE_TOPIC)

    r = rospy.Rate(1000)

    rospy.spin()

if __name__ == '__main__':
    main()