import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class Sim_time_sub(Node):
    def __init__(self):
        super().__init__('simple_time_sub')
        self.pub = self.create_subscription(Header, 'time', self.sub, 10)

    def sub(self, msg):
        self.get_logger().info(
            f'Recived time: {msg.stamp.sec}, {msg.stamp.nanosec}')
        self.get_logger().info(
            f'Recived frame_id: {msg.frame_id}')

def main():
    rclpy.init()
    node = Sim_time_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()