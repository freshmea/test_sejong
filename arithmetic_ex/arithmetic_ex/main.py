import rclpy
from rclpy.node import Node
from my_interfaces.msg import ArithmeticArgument
from my_interfaces.srv import ArithmeticOperator
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor


class Calculator(Node):
    def __init__(self):
        super().__init__('calculator')
        self.create_subscription(ArithmeticArgument, 'arithmtic_argument', self.sub, 10)
        self.create_service(ArithmeticOperator, 'arithmetic_operator', self.get_arithmetic_operator, callback_group=ReentrantCallbackGroup)
        
    def sub(self, msg):
        self.get_logger().info(f'Recived time: {msg.stamp.sec}, {msg.stamp.nanosec}')
        self.get_logger().info(f'Recived message: {msg.argument_a}, {msg.argument_b}')

def main():
    rclpy.init()
    node = Calculator()
    excutor = MultiThreadedExecutor(num_threads=4)
    excutor.add_node(node)
    try:
        excutor.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()