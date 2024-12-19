#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class RobotCmdROS(Node):
    def __init__(self):
        super().__init__('robot_cmd_ros')
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.rate = self.create_rate(10)
        self.get_logger().info('RobotCmdROS initialized')

    def begin(self):
        self.get_logger().info('Robot control started')

    def end(self):
        self.stop()
        self.get_logger().info('Robot control stopped')

    def stop(self):
        """Stop the robot."""
        twist = Twist()
        self.cmd_vel_pub.publish(twist)

    def forward(self, distance):
        """Move forward by the specified distance in meters."""
        speed = 0.2  # meters per second
        duration = distance / speed
        twist = Twist()
        twist.linear.x = speed

        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time).nanoseconds / 1e9 < duration:
            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

        self.stop()

    def backward(self, distance):
        """Move backward by the specified distance in meters."""
        speed = -0.2  # meters per second (negative for backward)
        duration = distance / abs(speed)
        twist = Twist()
        twist.linear.x = speed

        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time).nanoseconds / 1e9 < duration:
            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

        self.stop()

    def left(self, angle):
        """Rotate left by the specified angle in degrees."""
        angular_speed = 0.5  # radians per second
        duration = math.radians(angle) / angular_speed
        twist = Twist()
        twist.angular.z = angular_speed

        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time).nanoseconds / 1e9 < duration:
            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

        self.stop()

    def right(self, angle):
        """Rotate right by the specified angle in degrees."""
        angular_speed = -0.5  # radians per second (negative for right rotation)
        duration = math.radians(angle) / abs(angular_speed)
        twist = Twist()
        twist.angular.z = angular_speed

        start_time = self.get_clock().now()
        while (self.get_clock().now() - start_time).nanoseconds / 1e9 < duration:
            self.cmd_vel_pub.publish(twist)
            self.rate.sleep()

        self.stop()


def main():
    rclpy.init()
    robot = RobotCmdROS()

    try:
        robot.begin()
        robot.forward(1)
        robot.backward(1)
        robot.left(90)
        robot.right(90)
        robot.end()
    except KeyboardInterrupt:
        robot.get_logger().info('Interrupted by user')
        robot.end()
    finally:
        robot.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
