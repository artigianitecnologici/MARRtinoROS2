#!/usr/bin/env python3

# Copyright 2025 robotics-3d.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Ferrarini Fabio
# Email : ferrarini09@gmail.com
# File  : robot_cmd_ros.py 

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import time
from datetime import datetime
import math


class RobotCmdROS(Node):
    def __init__(self):
        super().__init__('robot_cmd_ros')
        # Topic definitions
        self.TOPIC_emotion = "social/emotion"
        self.TOPIC_gesture = "social/gesture"
        self.TOPIC_speech = "speech/to_speak"
        self.TOPIC_language = "speech/language"
        self.TOPIC_cmdvel = "cmd_vel"
        self.TOPIC_pan = "pan_controller/command"
        self.TOPIC_tilt = "tilt_controller/command"
        self.TOPIC_right_arm = "right_arm_controller/command"
        self.TOPIC_left_arm = "left_arm_controller/command"
        self.TOPIC_image = "/camera/image_raw"
        
        # Publisher definitions
        self.emotion_pub = self.create_publisher(String, self.TOPIC_emotion, 10)
        self.gesture_pub = self.create_publisher(String, self.TOPIC_gesture, 10)
        self.speech_pub = self.create_publisher(String, self.TOPIC_speech, 10)
        self.language_pub = self.create_publisher(String, self.TOPIC_language, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, self.TOPIC_cmdvel, 10)
        self.pan_pub = self.create_publisher(Float64, self.TOPIC_pan, 10)
        self.tilt_pub = self.create_publisher(Float64, self.TOPIC_tilt, 10)
        self.right_arm_pub = self.create_publisher(Float64, self.TOPIC_right_arm, 10)
        self.left_arm_pub = self.create_publisher(Float64, self.TOPIC_left_arm, 10)
        self.get_logger().info('RobotCmdROS initialized')
        # image
        self.bridge = CvBridge()
        self.cvimage = None
        #self.image_sub = self.create_subscription( Image, self.TOPIC_image, self.image_cb, 10)
        self.image_sub = self.create_subscription(    Image, self.TOPIC_image, self.image_cb, 10)

        self.get_logger().info(f"Subscribed to {self.TOPIC_image}")
        rclpy.spin_once(self, timeout_sec=1)  # Forza la prima esecuzione del callback

        self.logdir = os.path.expanduser("~/playground/log/")
        self.imagedir = os.path.expanduser("~/src/marrtinorobot2/marrtinorobot2_webinterface/www/viewer/img")
        if not os.path.isdir(self.logdir):
            self.logdir = os.path.expanduser("~/log/")
        if not os.path.isdir(self.logdir):
            self.logdir = "/tmp/"

    def begin(self):
        self.get_logger().info('Robot control started')

    def end(self):
        self.stop()
        self.get_logger().info('Robot control stopped')

    def stop(self):
        """Stop the robot."""
        twist = Twist()
        self.cmd_vel_pub.publish(twist)
        self.get_logger().info('Robot stopped')

    # image
    
    def image_cb(self, data):
        self.get_logger().info(f"Received an image: {data.header.stamp.sec}.{data.header.stamp.nanosec}")

        try:
            #self.cvimage = self.bridge.imgmsg_to_cv2(data, "bgr8")
            self.cvimage = self.bridge.imgmsg_to_cv2(data, desired_encoding="passthrough")

            self.get_logger().info("Image converted successfully!")
        except CvBridgeError as e:
            self.get_logger().error(f"CV Bridge error: {str(e)}")

    def get_image(self, sleep_time=3):
        self.get_logger().info("Acquiring image...")
        time.sleep(sleep_time)  # Attendere la ricezione di un frame
        if self.cvimage is None:
            self.get_logger().error("No image received!")
            return None

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
      
        img_path = os.path.join(self.imagedir, "lastimage.jpg")
        cv2.imwrite(img_path, self.cvimage)
        self.get_logger().info(f"Image saved at {img_path}")
        return self.cvimage
    
    def getImage(self):
        self.get_image(3)
         
    # movement

    def forward(self, distance):
        """Move forward by the specified distance in meters."""
        self.get_logger().info(f'Moving forward: {distance} meters')
        speed = 0.2  # meters per second
        duration = distance / speed
        twist = Twist()
        twist.linear.x = speed

        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.cmd_vel_pub.publish(twist)
            self.get_logger().info(f'Publishing: {twist}')
            rclpy.spin_once(self, timeout_sec=0.1)
        self.stop()

    def backward(self, distance):
        """Move backward by the specified distance in meters."""
        self.get_logger().info(f'Moving backward: {distance} meters')
        speed = -0.2  # meters per second (negative for backward)
        duration = distance / abs(speed)
        twist = Twist()
        twist.linear.x = speed

        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.cmd_vel_pub.publish(twist)
            self.get_logger().info(f'Publishing: {twist}')
            rclpy.spin_once(self, timeout_sec=0.1)
        self.stop()

    def left(self, angle):
        """Rotate left by the specified angle in degrees."""
        self.get_logger().info(f'Rotating left: {angle} degrees')
        angular_speed = 0.5  # radians per second
        duration = math.radians(angle) / angular_speed
        twist = Twist()
        twist.angular.z = angular_speed

        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.cmd_vel_pub.publish(twist)
            self.get_logger().info(f'Publishing: {twist}')
            rclpy.spin_once(self, timeout_sec=0.1)
        self.stop()

    def right(self, angle):
        """Rotate right by the specified angle in degrees."""
        self.get_logger().info(f'Rotating right: {angle} degrees')
        angular_speed = -0.5  # radians per second (negative for right rotation)
        duration = math.radians(angle) / abs(angular_speed)
        twist = Twist()
        twist.angular.z = angular_speed

        start_time = time.time()
        while (time.time() - start_time) < duration:
            self.cmd_vel_pub.publish(twist)
            self.get_logger().info(f'Publishing: {twist}')
            rclpy.spin_once(self, timeout_sec=0.1)
        self.stop()

    def gesture(self, msg):
        self.get_logger().info(f'gesture: {msg}')
        message = String()
        message.data = msg
        self.gesture_pub.publish(message)
    
    

    def say(self, msg,language):
        self.get_logger().info(f'speech: {msg}')
        self.get_logger().info(f'languahe: {language}')
        message = String()
        message.data = language
        self.language_pub.publish(message)
        message = String()
        message.data = msg
        self.speech_pub.publish(message)

    def emotion(self, msg):
        self.get_logger().info(f'social/emotion: {msg}')
        message = String()
        message.data = msg
        self.emotion_pub.publish(message)

    def pan(self, msg):
        self.get_logger().info(f'Pan Position: {msg}')
        message = Float64()
        message.data = float(msg)
        self.pan_pub.publish(message)

    def tilt(self, msg):
        self.get_logger().info(f'Tilt Position: {msg}')
        message = Float64()
        message.data = float(msg)
        self.tilt_pub.publish(message)

    def left_arm(self, msg):
        self.get_logger().info(f'Left Arm Position: {msg}')
        message = Float64()
        message.data = float(msg)
        self.left_arm_pub.publish(message)

    def right_arm(self, msg):
        self.get_logger().info(f'right Arm Position: {msg}')
        message = Float64()
        message.data = float(msg)
        self.right_arm_pub.publish(message)

    def head_position(self, msg):
        self.get_logger().info(f'Head Position: {msg}')
        if msg == 'front':
            self.pan(0)
            self.tilt(0)
        elif msg == 'left':
            self.pan(30)
            self.tilt(0)
        elif msg == 'right':
            self.pan(-30)
            self.tilt(0)
        elif msg == 'up':
            self.pan(0)
            self.tilt(-30)
        elif msg == 'down':
            self.pan(0)
            self.tilt(30)