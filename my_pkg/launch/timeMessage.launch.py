from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='my_pkg',
             executable='messagepub',
             output='screen'),
        Node(package='my_pkg',
             executable='messagesub1',
             output='screen'),
        Node(package='my_pkg',
             executable='messagesub2',
             output='screen'),
        Node(package='my_pkg',
             executable='simpletimepub',
             output='screen'),
        Node(package='my_pkg',
             executable='messagetimesub',
             output='screen')]
    )

