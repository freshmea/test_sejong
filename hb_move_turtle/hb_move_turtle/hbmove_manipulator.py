import rclpy
from rclpy.node import Node
from open_manipulator_msgs.srv import SetJointPosition, SetKinematicsPose


class Hbmove(Node):
    def __init__(self):
        super().__init__("manipulator_move")  # type: ignore
        self.create_timer(1 / 60, self.update_callback)
        self.clock = self.get_clock()
        self.prevtime = self.clock.now().nanoseconds
        self.goal_joint_space_req = SetJointPosition.Request()
        self.goal_joint_angle = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.goal_joint_space = self.create_client(
            SetJointPosition, "goal_joint_space_path"
        )
        self.stages = 0
        self.pathtime = 5

    def update_callback(self):
        if self.clock.now().nanoseconds - self.prevtime > self.pathtime * 1000000000:
            self.prevtime = self.clock.now().nanoseconds
            self.stages += 1
            if self.stages > 25:
                self.stages = 0
            self.get_logger().info(f"stages: {self.stages}")
        # 초기 위치
        if self.stages == 0:
            self.goal_joint_angle[0] = 0.0
            self.goal_joint_angle[1] = 0.0
            self.goal_joint_angle[2] = 0.0
            self.goal_joint_angle[3] = 0.0
            self.pathtime = 3.0
            self.send_goal_joint_space(self.pathtime)
        # 초기 위치2
        if self.stages == 1:
            self.goal_joint_angle[0] = 0.0
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 3.0
            self.send_goal_joint_space(self.pathtime)
        # 좌우 흔들기 4 번
        if self.stages == 2:
            self.goal_joint_angle[0] = 0.637
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 3:
            self.goal_joint_angle[0] = -0.463
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 4:
            self.goal_joint_angle[0] = 0.637
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 5:
            self.goal_joint_angle[0] = -0.463
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 6:
            self.goal_joint_angle[0] = 0.637
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 7:
            self.goal_joint_angle[0] = -0.463
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 8:
            self.goal_joint_angle[0] = 0.637
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 9:
            self.goal_joint_angle[0] = -0.463
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        # 위 아래 흔들기 4 번
        if self.stages == 10:
            self.goal_joint_angle[0] = -0.002
            self.goal_joint_angle[1] = -0.744
            self.goal_joint_angle[2] = -0.202
            self.goal_joint_angle[3] = 1.068
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 11:
            self.goal_joint_angle[0] = 0.071
            self.goal_joint_angle[1] = -0.945
            self.goal_joint_angle[2] = 0.535
            self.goal_joint_angle[3] = -0.431
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 12:
            self.goal_joint_angle[0] = -0.002
            self.goal_joint_angle[1] = -0.744
            self.goal_joint_angle[2] = -0.202
            self.goal_joint_angle[3] = 1.068
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 13:
            self.goal_joint_angle[0] = 0.071
            self.goal_joint_angle[1] = -0.945
            self.goal_joint_angle[2] = 0.535
            self.goal_joint_angle[3] = -0.431
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 14:
            self.goal_joint_angle[0] = -0.002
            self.goal_joint_angle[1] = -0.744
            self.goal_joint_angle[2] = -0.202
            self.goal_joint_angle[3] = 1.068
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 15:
            self.goal_joint_angle[0] = 0.071
            self.goal_joint_angle[1] = -0.945
            self.goal_joint_angle[2] = 0.535
            self.goal_joint_angle[3] = -0.431
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 16:
            self.goal_joint_angle[0] = -0.002
            self.goal_joint_angle[1] = -0.744
            self.goal_joint_angle[2] = -0.202
            self.goal_joint_angle[3] = 1.068
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 17:
            self.goal_joint_angle[0] = 0.071
            self.goal_joint_angle[1] = -0.945
            self.goal_joint_angle[2] = 0.535
            self.goal_joint_angle[3] = -0.431
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        # 서서 회전하기 4 번
        if self.stages == 18:
            self.goal_joint_angle[0] = 1.344
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 19:
            self.goal_joint_angle[0] = -1.855
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 20:
            self.goal_joint_angle[0] = 1.344
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 21:
            self.goal_joint_angle[0] = -1.855
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 22:
            self.goal_joint_angle[0] = 1.344
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 23:
            self.goal_joint_angle[0] = -1.855
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 24:
            self.goal_joint_angle[0] = 1.344
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)
        if self.stages == 25:
            self.goal_joint_angle[0] = -1.855
            self.goal_joint_angle[1] = 0.046
            self.goal_joint_angle[2] = -1.456
            self.goal_joint_angle[3] = 0.518
            self.pathtime = 0.5
            self.send_goal_joint_space(self.pathtime)

    def send_goal_joint_space(self, path_time):
        self.goal_joint_space_req.joint_position.joint_name = [
            "joint1",
            "joint2",
            "joint3",
            "joint4",
            "gripper",
        ]
        self.goal_joint_space_req.joint_position.position = [
            self.goal_joint_angle[0],
            self.goal_joint_angle[1],
            self.goal_joint_angle[2],
            self.goal_joint_angle[3],
            self.goal_joint_angle[4],
        ]
        self.goal_joint_space_req.path_time = path_time

        try:
            self.goal_joint_space.call_async(self.goal_joint_space_req)
        except Exception as e:  # noqa
            self.get_logger().info("Sending Goal Joint failed %r" % (e,))


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
