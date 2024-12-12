import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Quaternion
from sensor_msgs.msg import Imu
import numpy as np

class MotionControl(Node):
    def __init__(self):
        super().__init__('motion_control')
        self.subscription_imu = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10)
        self.subscription_imu
        self.publisher_cmd_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        self.current_orientation = None

    def imu_callback(self, msg):
        orientation = msg.orientation
        # Convert quaternion to Euler angles
        roll, pitch, yaw = self.quaternion_to_euler(
            orientation.x, orientation.y, orientation.z, orientation.w)
        self.current_orientation = yaw

    def quaternion_to_euler(self, x, y, z, w):
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = np.arctan2(t0, t1)
        
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = np.arcsin(t2)
        
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = np.arctan2(t3, t4)
        
        return roll, pitch, yaw

    def move_forward(self, distance):
        cmd_msg = Twist()
        cmd_msg.linear.x = 0.2  # Adjust linear velocity as needed
        start_position = self.get_robot_position()
        current_distance = 0
        while current_distance < distance:
            self.publisher_cmd_vel.publish(cmd_msg)
            rclpy.spin_once(self)
            current_position = self.get_robot_position()
            current_distance = np.sqrt((current_position[0] - start_position[0])**2 + (current_position[1] - start_position[1])**2)
        cmd_msg.linear.x = 0
        self.publisher_cmd_vel.publish(cmd_msg)

    def turn(self, angle):
        cmd_msg = Twist()
        cmd_msg.angular.z = np.sign(angle) * 0.5  # Adjust angular velocity as needed
        start_angle = self.current_orientation
        target_angle = start_angle + np.deg2rad(angle)
        while np.abs(self.current_orientation - start_angle) < np.abs(angle):
            self.publisher_cmd_vel.publish(cmd_msg)
            rclpy.spin_once(self)
        cmd_msg.angular.z = 0
        self.publisher_cmd_vel.publish(cmd_msg)

    def get_robot_position(self):
        # Here you should implement the logic to get the robot's current position
        # For simplicity, I assume it returns a tuple (x, y) representing the position
        return (0, 0)  # Change this according to your robot's localization method

def main(args=None):
    rclpy.init(args=args)
    motion_control = MotionControl()

    # Move forward by 1 meter
    motion_control.move_forward(1)

    # Turn right by 90 degrees
    motion_control.turn(90)

    # Move forward by 1 meter
    motion_control.move_forward(1)

    # Turn left by 90 degrees
    motion_control.turn(-90)

    motion_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
