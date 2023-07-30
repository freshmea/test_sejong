import rclpy
from rclpy.node import Node
from rclpy.clock import Clock, ClockType
from std_msgs.msg import Header

class Sim_time_pub(Node):
    def __init__(self):
        super().__init__('tpub')
        self.pub = self.create_publisher(Header, 'time', 10)
        self.create_timer(0.1, self.publisher)
        self.id = 0
        self.clock = Clock(clock_type=ClockType.STEADY_TIME)
        
    def publisher(self):
        msg = Header()
        msg.stamp = self.clock.now().to_msg()
        msg.frame_id = str(self.id)
        self.id += 1
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = Sim_time_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()