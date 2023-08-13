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
        self.create_service(ArithmeticOperator, 'arithmetic_operator', self.get_arithmetic_operator, callback_group=ReentrantCallbackGroup())
        self.argument_a = 0.0
        self.argument_b = 0.0
        
    def sub(self, msg):
        self.get_logger().info(f'Recived time: {msg.stamp.sec}, {msg.stamp.nanosec}')
        self.get_logger().info(f'Recived message: {msg.argument_a}, {msg.argument_b}')
        self.argument_a = msg.argument_a
        self.argument_b = msg.argument_b

    def get_arithmetic_operator(self, request, response):
        self.argument_operator = request.arithmetic_operator
        if self.argument_operator == ArithmeticOperator.Request.PLUS:
            response.arithmetic_result = self.argument_a + self.argument_b
        if self.argument_operator == ArithmeticOperator.Request.MINUS:
            response.arithmetic_result = self.argument_a - self.argument_b
        if self.argument_operator == ArithmeticOperator.Request.MULTIPLY:
            response.arithmetic_result = self.argument_a * self.argument_b
        if self.argument_operator == ArithmeticOperator.Request.DIVISION:
            if self.argument_b == 0.0 :
                response.arithmetic_result = 0.0
            else:
                response.arithmetic_result = self.argument_a / self.argument_b
        self.get_logger().info(f'Reciving Service {self.argument_operator}')
        return response
    
def main():
    rclpy.init()
    node = Calculator()
    excutor = MultiThreadedExecutor(num_threads=4)
    excutor.add_node(node)
    try:
        excutor.spin()
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        excutor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()