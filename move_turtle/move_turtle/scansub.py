import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
import numpy as np
import random

MAX_SLICE = 8
FORWARD_SPEED = 0.07


class Sim_sub(Node):
    def __init__(self):
        super().__init__("scansub")  # type: ignore
        self.create_subscription(LaserScan, "scan", self.sub, qos_profile_sensor_data)
        self.twistpub = self.create_publisher(Twist, "cmd_vel", 10)
        self.create_timer(0.01, self.pub)
        self.create_timer(0.01, self.update)
        self.msg = Twist()
        self.max_value = 0.0
        self.max_index = 0
        self.scan_avr = [1.0 for i in range(MAX_SLICE)]
        self.wall_detect = False

    def sub(self, msg: LaserScan):
        # find maxium value and index
        self.max_value = 0.0
        self.max_index = 0

        # 모든 방향에 대해서 무한 값은 3.5로 바꾸고, 가장 먼 거리를 찾아서 변수에 저장
        for i in range(360):
            if msg.ranges[i] == float("inf"):
                msg.ranges[i] = 3.5
            if msg.ranges[i] > self.max_value:
                self.max_value = msg.ranges[i]
                self.max_index = i
        # MAX_SLICE 각도로 나눠서 각 방향의 평균값을 구함
        for i in range(MAX_SLICE):
            self.scan_avr[i] = float(
                np.average(
                    msg.ranges[i * (360 // MAX_SLICE) : (i + 1) * (360 // MAX_SLICE)]
                )
            )
        self.get_logger().info(f"max_index: {self.max_index}")
        for i in range(MAX_SLICE):
            self.get_logger().info(f"scan_avr[{i}]: {self.scan_avr[i]}")

    def pub(self):
        self.twistpub.publish(self.msg)
        pass

    def update(self):
        # 벽을 찾은 후에는 벽을 따라가도록 함
        if self.wall_detect:
            # 앞쪽 방향에 장애물이 있는지 확인
            if np.average([self.scan_avr[0], self.scan_avr[7]]) < 0.4:  # type: ignore
                self.msg.angular.z = 0.5
                self.msg.linear.x = 0.0
            else:
                # 오른쪽 방향에 벽이 먼면 우회전 아니면 좌회전 적당한거리(0.3~0.4)면 직진
                if self.scan_avr[6] > 0.2:
                    self.msg.angular.z = -0.2
                    self.msg.linear.x = FORWARD_SPEED / 2
                elif self.scan_avr[6] < 0.18:
                    self.msg.angular.z = 0.6
                    self.msg.linear.x = FORWARD_SPEED / 2
                else:
                    self.msg.angular.z = 0.0
                    self.msg.linear.x = FORWARD_SPEED
                # 충돌 체크
                if (
                    self.scan_avr[0] < 0.15
                    or self.scan_avr[7] < 0.15
                    or self.scan_avr[1] < 0.15
                    or self.scan_avr[6] < 0.15
                ):
                    self.msg.linear.x = -FORWARD_SPEED
                    # 뒤로 갈 수 없다면 제자리 회전
                    if self.scan_avr[3] < 0.1 or self.scan_avr[4] < 0.1:
                        self.msg.linear.x = 0.0
                    self.msg.angular.z = random.random() * 0.5
                    self.get_logger().info("collision detected")

        else:
            # 벽을 찾기 전에는 직진
            self.msg.linear.x = FORWARD_SPEED
            # 벽을 찾으면 벽 찾음 변수 True로 바꿈
            if (
                (self.scan_avr[6] < 0.4)
                or (self.scan_avr[7] < 0.4)
                or (self.scan_avr[0] < 0.4)
            ):
                self.wall_detect = True
                self.get_logger().info("wall detected")


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
