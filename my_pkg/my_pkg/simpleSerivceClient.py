import rclpy
import random
from rclpy.node import Node 
from my_interfaces.srv import TwoIntAdd

class Simple_service_client(Node):
    def __init__(self):
        super().__init__('twonumber_cli')
        self.client = self.create_client(TwoIntAdd, 'addtwoint')
    
    def call_service(self):
        self.msg = TwoIntAdd.Request()
        self.msg.a_number = random.randint(0,200)
        self.msg.b_number = random.randint(0,200)
        
        self.future = self.client.call_async(self.msg)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main():
    rclpy.init()
    node = Simple_service_client()
    try:
        response = node.call_service()
        node.get_logger().info( f'Recived message : {response.return_number}')
        # rclpy.spin(node)
    except:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main':
    main()
