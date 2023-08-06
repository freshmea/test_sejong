import rclpy
from rclpy.node import Node 
from my_interfaces.srv import TwoIntAdd

class Simple_service_server(Node):
    def __init__(self):
        super().__init__('twonumber')
        self.create_service(TwoIntAdd, 'addtwoint', self.twonumber_callback)
        
    def twonumber_callback(self, request, response):
        self.get_logger().info(f'incomming data{request.a_numebr}, {request.b_number}')
        response.return_number =  request.a_number + request.b_number
        return response

def main():
    rclpy.init()
    node = Simple_service_server()
    try:
        rclpy.spin(node)
    except:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main':
    main()
