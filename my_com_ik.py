#!/usr/bin/env python
import rospy
import math
import serial
import time
import tf2_ros
import sys

from geometry_msgs.msg import Twist
from std_msgs.msg import String
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg

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
    rospy.wait_for_service('compute_ik')
    compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)

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
    request = GetPositionIKRequest()
    self.xyz = input.transform.translation
        #add value 0 or 1 to indicate object type
        li = [self.xyz.x,self.xyz.y,self.xyz.z]
    request.ik_request.group_name = "manipulator"
    request.ik_request.ik_link_name = link
    request.ik_request.attempts = 20
    request.ik_request.pose_stamped.header.frame_id = "base_link"
    request.ik_request.pose_stamped.pose.position.x = self.xyz.x
    request.ik_request.pose_stamped.pose.position.y = self.xyz.y
    request.ik_request.pose_stamped.pose.position.z = self.xyz.z
    request.ik_request.pose_stamped.pose.orientation.x = 0.0
    request.ik_request.pose_stamped.pose.orientation.y = 1.0
    request.ik_request.pose_stamped.pose.orientation.z = 0.0
    request.ik_request.pose_stamped.pose.orientation.w = 0.0
    response = compute_ik(request)
    li = response.joint_state.position
    li_degree = [ int(rad * 180 / math.pi) - 90)  for rad in li ]
    li_degree.append(self.obj_type)
    my_str = str(li_degree).strip('[]') + "a"
    print(my_str)
    self.ser.write(my_str)

if __name__ == '__main__':
  node_parser = MyCom(sys.argv[1], sys.argv[2])
  node_parser.start_subscribe_string()
