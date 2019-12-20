#!/usr/bin/env python
#The line above tells Linux that this file is a Python script,
#and that the OS should use the Python interpreter in /usr/bin/env
#to run it. Don't forget to use "chmod +x [filename]" to make
#this script executable.

#Import the rospy package. For an import to work, it must be specified
#in both the package manifest AND the Python file in which it is used.
import rospy
import tf2_ros
import sys

from geometry_msgs.msg import Twist

trans_red = None
trans_blue = None

#Define the method which contains the main functionality of the node.
def broadcaster():
  """
  Controls a turtlebot whose position is denoted by turtlebot_frame,
  to go to a position denoted by target_frame
  Inputs:
  - turtlebot_frame: the tf frame of the AR tag on your turtlebot
  - target_frame: the tf frame of the target AR tag
  """

  ################################### YOUR CODE HERE ##############

  #Create a publisher and a tf buffer, which is primed with a tf listener
  tfBuffer = tf2_ros.Buffer()
  tfListener = tf2_ros.TransformListener(tfBuffer)
  br = tf2_ros.TransformBroadcaster()
  
  # Create a timer object that will sleep long enough to result in
  # a 10Hz publishing rate
  r = rospy.Rate(10) # 10hz

  found_red = False
  found_blue = False

  global trans


  # Loop until the node is killed with Ctrl-C
  while not rospy.is_shutdown():
    try:
      if not found_red or not found_blue:
        # Add tf2 transform broadcaster
        if not found_red:
          trans_red = tfBuffer.lookup_transform("map", "object_1green_1", rospy.Time())
          trans_red.child_frame_id = "copy_frame_red"
          br.sendTransform(trans_red)
          found_red = True
        if not found_blue:
          trans_blue = tfBuffer.lookup_transform("map", "object_1blue_1", rospy.Time())
          trans_blue.child_frame_id = "copy_frame_blue"
          br.sendTransform(trans_blue)
          found_blue = True
      else:
        trans_red.header.stamp = rospy.Time.now()
        trans_blue.header.stamp = rospy.Time.now()
        br.sendTransform(trans_red)
        br.sendTransform(trans_blue)
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
      print(found_red, found_blue)
    # Use our rate object to sleep until it is time to publish again
    r.sleep()

      
# This is Python's sytax for a main() method, which is run by default
# when exectued in the shell
if __name__ == '__main__':
  # Check if the node has received a signal to shut down
  # If not, run the talker method

  #Run this program as a new node in the ROS computation graph 
  #called /turtlebot_controller.
  rospy.init_node('broadcaster', anonymous=True)

  try:
    broadcaster()
  except rospy.ROSInterruptException:
    pass
