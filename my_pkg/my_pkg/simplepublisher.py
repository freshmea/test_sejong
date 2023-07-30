import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from rclpy.qos import QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from std_msgs.msg import String
from rclpy.qos import qos_profile_sensor_data

class Sim_pub(Node):
    def __init__(self):
        super().__init__('simple_mpub')
        # qos_profile = QoSProfile(
        #     history = QoSHistoryPolicy.KEEP_ALL, 
        #     reliability = QoSReliabilityPolicy.RELIABLE,
        #     durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
        #     )
        self.pub = self.create_publisher(String, 'message', qos_profile_sensor_data)
        self.create_timer(1, self.publisher)
        self.count = 0

    def publisher(self):
        msg = String()
        msg.data = 'hellow :'+str(self.count)
        self.pub.publish(msg)
        self.count += 1

def main():
    rclpy.init()
    node = Sim_pub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()