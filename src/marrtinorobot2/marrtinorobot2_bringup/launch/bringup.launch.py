from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.conditions import IfCondition, UnlessCondition


def generate_launch_description():
   

    description_launch_path = PathJoinSubstitution(
        [FindPackageShare('marrtinorobot2_description'), 'launch', 'description.launch.py']
    )


    ekf_config_path = PathJoinSubstitution(
        [FindPackageShare("marrtinorobot2_base"), "config", "ekf.yaml"]
    )

    default_robot_launch_path = PathJoinSubstitution(
        [FindPackageShare('marrtinorobot2_bringup'), 'launch', 'marrtino2_robot.launch.py']
    )


  
    return LaunchDescription([


        DeclareLaunchArgument(
            name='base_serial_port', 
            default_value='/dev/ttyACM0',
            description='MARRtino robot Base Serial Port'
        ),

        DeclareLaunchArgument(
            name='odom_topic', 
            default_value='/odom',
            description='EKF out odometry topic'
        ),
        
       
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                ekf_config_path
            ],
            remappings=[("odometry/filtered", LaunchConfiguration("odom_topic"))]
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(default_robot_launch_path),
            
            launch_arguments={
                'base_serial_port': LaunchConfiguration("base_serial_port")
            }.items()
        ) 

   
    ])
