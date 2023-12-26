from re import A
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

LIN_MAX = 0.22
ANG_MAX = 2.84
MAX_SLICE = 8


class Hbmove(Node):
    def __init__(self):
        super().__init__("move_turtlenot")  # type: ignore
        self.create_timer(0.1, self.turtle_callback)
        self.create_timer(1 / 60, self.update)
        self.pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_subscription(LaserScan, "scan", self.scan_callback, 10)
        self.scan = LaserScan()
        self.scan_avg = [0.0 for _ in range(MAX_SLICE)]
        self.msg = Twist()

    def update(self):
        # update variables self.msg, self.scan, self.camera
        if sum([self.scan_avg[0], self.scan_avg[7]]) < 1:
            self.msg.linear.x = 0.0
            self.get_logger().info(
                f"Set stop msg: {sum([self.scan_avg[0], self.scan_avg[7]])}"
            )
        else:
            self.msg.linear.x = LIN_MAX
            self.get_logger().info(
                f"Set go msg: {sum([self.scan_avg[0], self.scan_avg[7]])}"
            )

    def turtle_callback(self):
        self.msg = self.speed_limit(self.msg)
        self.pub.publish(self.msg)

    def speed_limit(self, msg: Twist):
        if msg.linear.x > LIN_MAX:
            msg.linear.x = LIN_MAX
        elif msg.linear.x < -LIN_MAX:
            msg.linear.x = -LIN_MAX
        if msg.angular.z > ANG_MAX:
            msg.angular.z = ANG_MAX
        elif msg.angular.z < -ANG_MAX:
            msg.angular.z = -ANG_MAX
        return msg

    def scan_callback(self, msg: LaserScan):
        self.scan = msg
        # self.scan_avg[0] = sum(msg.ranges[0:45])/45
        # self.scan_avg[1] = sum(msg.ranges[45:90])/45
        # self.scan_avg[2] = sum(msg.ranges[90:135])/45
        # self.scan_avg[3] = sum(msg.ranges[135:180])/45
        # self.scan_avg[4] = sum(msg.ranges[180:225])/45
        # self.scan_avg[5] = sum(msg.ranges[225:270])/45
        # self.scan_avg[6] = sum(msg.ranges[270:315])/45
        # self.scan_avg[7] = sum(msg.ranges[315:360])/45
        for i in range(MAX_SLICE):
            self.scan_avg[i] = sum(
                msg.ranges[i * (360 // MAX_SLICE) : (i + 1) * (360 // MAX_SLICE)]
            ) / (360 // MAX_SLICE)
        for i, v in enumerate(self.scan_avg):
            self.get_logger().info(f"Recived msg[{i}]: {v}")


def main():
    rclpy.init()
    node = Hbmove()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
