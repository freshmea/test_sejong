import rclpy
from rclpy.node import Node
from my_interfaces.msg import ArithmeticArgument

class Arugument_sub(Node):
    def __init__(self):
        super().__init__('argument_sub')
        self.create_subscription(ArithmeticArgument, 'arithmetic_argument', self.sub, 10)
    def sub(self, msg):
        self.get_logger().info(f'Recived time: {msg.stamp.sec}, {msg.stamp.nanosec}')
        self.get_logger().info(f'Recived message: {msg.argument_a}, {msg.argument_b}')

def main():
    rclpy.init()
    node = Arugument_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()