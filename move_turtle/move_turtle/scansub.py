import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
import numpy as np

MAX_SLICE = 8


class Sim_sub(Node):
    def __init__(self):
        super().__init__("scansub")  # type: ignore
        self.create_subscription(LaserScan, "scan", self.sub, qos_profile_sensor_data)
        self.twistpub = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_timer(0.1, self.pub)
        self.create_timer(0.01, self.update)
        self.msg = Twist()
        self.max_value = 0.0
        self.max_index = 0
        self.scan_avr = list(range(MAX_SLICE))

    def sub(self, msg: LaserScan):
        # find maxium value and index
        self.max_value = 0.0
        self.max_index = 0
        for i in range(360):
            if msg.ranges[i] == float("inf"):
                msg.ranges[i] = 3.5
            if msg.ranges[i] > self.max_value:
                self.max_value = msg.ranges[i]
                self.max_index = i
        for i in range(MAX_SLICE):
            self.scan_avr[i] = np.average(
                msg.ranges[i * (360 // MAX_SLICE) : (i + 1) * (360 // MAX_SLICE)]
            )
        self.get_logger().info(f"max_index: {self.max_index}")
        for i in range(MAX_SLICE):
            self.get_logger().info(f"scan_avr[{i}]: {self.scan_avr[i]}")

    def pub(self):
        self.twistpub.publish(self.msg)
        pass

    def update(self):
        # if self.max_index > 350 or self.max_index < 10:
        #     self.msg.angular.z = 0.0
        #     self.msg.linear.x = 0.1
        # elif self.max_index > 180:
        #     self.msg.angular.z = -0.5
        #     self.msg.linear.x = 0.0
        # elif self.max_index < 180:
        #     self.msg.angular.z = 0.5
        #     self.msg.linear.x = 0.0

        if np.average([self.scan_avr[0], self.scan_avr[7]]) < 0.4:
            self.msg.angular.z = 0.5
            self.msg.linear.x = 0.0
        else:
            if self.scan_avr[6] > 0.4:
                self.msg.angular.z = -0.5
            elif self.scan_avr[6] < 0.3:
                self.msg.angular.z = 0.5
            else:
                self.msg.angular.z = 0.0
            self.msg.linear.x = 0.05
        # if self.left_side_avr > 0.2:
        #     self.msg.angular.z = 0.5
        #     self.msg.linear.x = 0.0


def main():
    rclpy.init()
    node = Sim_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("keyboard Interrupt!!")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
