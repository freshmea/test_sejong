
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
import os

def generate_launch_description():
    return LaunchDescription([
        Node(package='arithmetic_ex',
             executable='argument',
             parameters=[{'min_random_num': 10, 'max_random_num': 50}],
             output='screen')
    ])
