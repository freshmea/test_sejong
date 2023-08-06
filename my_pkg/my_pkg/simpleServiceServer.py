import rclpy
from rclpy.node import Node 

class Simple_service_server(Node):
    def __init__(self):
        super().__init__('twonumber')
        self.create_service()

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
