import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from ros2_aruco_interfaces.msg import ArucoMarkers
from math import sqrt, atan2

MAX_LIN_VEL = 0.22
MAX_ANG_VEL = 2.84


class Move_with_angle(Node):
    def __init__(self):
        super().__init__("straight_with_angle")
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.odometery_sub = self.create_subscription(
            Odometry, "odom", self.odom_sub, 10
        )
        self.aruco_marker_sub = self.create_subscription(
            ArucoMarkers, "aruco_markers", self.aruco_sub, 10
        )
        self.update_timer = self.create_timer(0.1, self.update)
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.x = 0.0
        self.y = 0.0
        self.moving = False
        self.distance = 0.0
        self.angle = 0.0

    def odom_sub(self, data):
        self.x = data.pose.pose.position.x
        self.y = data.pose.pose.position.y

    def aruco_sub(self, submsg):
        self.distance = submsg.poses[0].position.z - 0.05
        self.angle = atan2(
            submsg.poses[0].position.y - self.y, submsg.poses[0].position.x - self.x
        )
        self.origin_x = self.x
        self.origin_y = self.y
        self.moving = True

    def update(self):
        msg = Twist()
        if self.moving:
            if origin_y > 추종값 - tolerance_error:
                msg.angular.z = -0.5
            elif origin_y < 추종값 + tolerance_error:
                msg.angular.z = 0.5
            # Calculate angle error
            angle_error = self.angle - self.get_yaw()

            # Calculate linear velocity
            msg.linear.x = min(MAX_LIN_VEL, self.distance)

            # Calculate angular velocity
            msg.angular.z = -angle_error * MAX_ANG_VEL

            # Publish the twist message
            self.pub.publish(msg)
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.pub.publish(msg)

    def get_yaw(self):
        # TODO: Implement this function to get the current yaw angle of the robot
        pass

    def restrain(self, msg):
        if msg.linear.x < -MAX_LIN_VEL:
            msg.linear.x = -MAX_LIN_VEL
        elif msg.linear.x > MAX_LIN_VEL:
            msg.linear.x = MAX_LIN_VEL
        if msg.angular.z < -MAX_ANG_VEL:
            msg.angular.z = -MAX_ANG_VEL
        elif msg.angular.z > MAX_ANG_VEL:
            msg.angular.z = MAX_ANG_VEL
        return msg


def main():
    rclpy.init()
    node = Move_with_angle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("keyboard Interrupt!!")
    finally:
        # stop code
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        node.pub.publish(msg)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
