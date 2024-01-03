import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Hbmove(Node):
    def __init__(self):
        super().__init__("minimal_publisher")  # type: ignore
        self.pub = self.create_subscription(
            String, "hello", self.hello_sub_callback, 10
        )
        self.count = 0

    def hello_sub_callback(self, msg):
        self.get_logger().info("I heard: " + msg.data)
        self.get_logger().error("Test error")


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
