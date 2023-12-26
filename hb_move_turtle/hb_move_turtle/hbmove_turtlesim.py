import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Hbmove(Node):
    def __init__(self):
        super().__init__("move_turtlesim")  # type: ignore
        self.create_timer(0.1, self.turtle_callback)
        self.pub = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        self.count = 0

    def turtle_callback(self):
        msg = Twist()
        msg.linear.x = 1.0
        msg.angular.z = 1.0
        self.pub.publish(msg)
        self.count += 1


def main():
    rclpy.init()
    node = Hbmove()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
