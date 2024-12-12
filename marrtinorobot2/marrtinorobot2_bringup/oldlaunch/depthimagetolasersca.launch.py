from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan_node',
            remappings=[('depth','/stereo/depth'),
                        ('depth_camera_info', '/stereo/camera_info'),
                        ('scan', '/oak_scan')],
            parameters=[{
                'scan_time': 0.033,    
                'range_min': 0.45,   #the minimum distance unit of the projection point (in meters), and the closer ones are discarded 
                'range_max': 5.0,   #the maximum distance unit of the projection point (in meters), with further points discarded 
                'scan_height': 5,    #depthimage used for conversion into laserscan rows of 
                'output_frame': 'camera_depth_optical_frame'  #published frames ID
            }]
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='depthimage_to_laserscan_tf',
            arguments=['0','0','0','0','0','0','1','oak-d_frame','camera_depth_optical_frame']
        )
    ])
