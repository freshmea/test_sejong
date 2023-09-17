import rclpy
import random
from rclpy.node import Node
from my_interfaces.msg import ArithmeticArgument
from rcl_interfaces.msg import SetParametersResult

class Argument(Node):
    def __init__(self):
        super().__init__('argument')
        # 파라미터 설정.
        self.declare_parameter('min_random_num', 0)
        self.min_random_num = self.get_parameter('min_random_num').value
        self.declare_parameter('max_random_num', 100)
        self.max_random_num = self.get_parameter('max_random_num').value
        self.add_on_set_parameters_callback(self.update_parameter)
        self.pub = self.create_publisher(ArithmeticArgument, 'arithmetic_argument', 10)
        self.timer = self.create_timer(1, self.publisher)

    def publisher(self):
        msg = ArithmeticArgument()
        msg.stamp = self.get_clock().now().to_msg()
        msg.argument_a = float(random.randint(self.min_random_num, self.max_random_num))
        msg.argument_b = float(random.randint(self.min_random_num, self.max_random_num))
        print(msg.argument_a, msg.argument_b)
        self.pub.publish(msg)

    def update_parameter(self, params):
        for param in params:
            if param.name == 'min_random_num':
                self.min_random_num = param.value
            if param.name == 'max_random_num':
                self.max_random_num = param.value
        return SetParametersResult(successful=True)

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