import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Argument(Node):
    def __init__(self):
        super().__init__('msub')
        self.create_subscription(String, 'message', self.sub, 10)
    def sub(self, msg):
        self.get_logger().info(f'Recived message: {msg.data}')

def main():
    rclpy.init()
    node = Argument()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()