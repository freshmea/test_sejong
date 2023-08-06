import rclpy
from rclpy.node import Node 
from my_interfaces.srv import TwoIntAdd
from rclpy.action import ActionServer

class Fibonacci_action_server(Node):
    def __init__(self):
        super().__init__('fibonacci_server')
        self.action_server = ActionServer(self, )

    def twonumber_callback(self, request, response):
        print(type(request))
        # self.get_logger().info(f'incomming data{self.request.a}, {self.request.b}')
        # response.rn =  request.a + request.b
        # response.rn = 10 
        return response
        

    def test(self):
        self.get_logger().info( f'a {self.cnt}')
        self.cnt += 1

def main(args = None):
    rclpy.init(args = args)
    node = Fibonacci_action_server()
    try:
        rclpy.spin(node)
    except:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main':
    main()
