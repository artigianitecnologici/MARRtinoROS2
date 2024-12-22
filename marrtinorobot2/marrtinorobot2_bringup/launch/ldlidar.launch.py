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
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            name='topic_name', 
            default_value='scan',
            description='Laser Topic Name'
        ),

        DeclareLaunchArgument(
            name='frame_id', 
            default_value='laser',
            description='Laser Frame ID'
        ),

        DeclareLaunchArgument(
            name='lidar_transport',
            default_value='serial',
            description='Lidar transport: serial, udp_server, udp_client, tcp_server, tcp_client'
        ),

        DeclareLaunchArgument(
            name='lidar_serial_port',
            default_value='/dev/ttyUSB0',
            description='Lidar serial port device name'
        ),

        DeclareLaunchArgument(
            name='lidar_server_ip',
            default_value='0.0.0.0',
            description='Lidar server ip'
        ),

        DeclareLaunchArgument(
            name='lidar_server_port',
            default_value='8889',
            description='Lidar server port number'
        ),

       
        
        Node(
            package='ldlidar_stl_ros2',
            executable='ldlidar_stl_ros2_node',
            name='ld19',
            output='screen',
            parameters=[
                {'product_name': 'LDLiDAR_LD19'},
                {'topic_name': LaunchConfiguration('topic_name')},
                {'frame_id': LaunchConfiguration('frame_id')},
                {'comm_mode': LaunchConfiguration('lidar_transport')},
                {'port_name': LaunchConfiguration('lidar_serial_port')},
                {'port_baudrate': 230400},
                {'server_ip': LaunchConfiguration('lidar_server_ip')},
                {'server_port': LaunchConfiguration('lidar_server_port')},
                {'laser_scan_dir': True},
                {'bins': 498},
                {'enable_angle_crop_func': False},
                {'angle_crop_min': 135.0},
                {'angle_crop_max': 225.0}
            ]
        )
    ])

