#!/usr/bin/env python
import rospy
import math
import serial
import time
import tf2_ros
import sys

from geometry_msgs.msg import Twist
from std_msgs.msg import String

class MyCom:
  xyz = []

  def __init__(self, turtlebot_frame, goal_frame):
    rospy.init_node('my_com');
    self.ser = serial.Serial('/dev/ttyACM0',9600)
    self.ser.flushInput()
    self.tfBuffer = tf2_ros.Buffer()
    self.tfListener = tf2_ros.TransformListener(self.tfBuffer)
    self.turtlebot_frame = turtlebot_frame
    self.goal_frame = goal_frame
    self.obj_type = 0

  def start_subscribe_string(self):
    rospy.Subscriber("/notify_7bot", String, self.callback_string)
    rospy.spin()

  def callback_string(self, input):
    my_str = input.data
    if my_str is "blue":
      self.obj_type = 1
    node_parser.find_tf()

  def find_tf(self):
    r = rospy.Rate(10) # 10hz
    x = True
    while x:
	   try:
	      self.trans = self.tfBuffer.lookup_transform(self.turtlebot_frame, self.goal_frame, rospy.Time())
              print(self.trans)
	      self.move(self.trans)
              x = False
	   except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
	      pass
	   r.sleep()

  def move(self, input):
    self.xyz = input.transform.translation
    #add value 0 or 1 to indicate object type
    li = [self.xyz.x,self.xyz.y,self.xyz.z]
    li.append(self.obj_type)
    my_str = str(li).strip('[]') + "a"
    print(my_str)
    self.ser.write(my_str)

if __name__ == '__main__':
  node_parser = MyCom(sys.argv[1], sys.argv[2])
  node_parser.start_subscribe_string()
