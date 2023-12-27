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

    def update_callback(self):
        if self.clock.now().nanoseconds - self.prevtime > 5000000000:
            self.prevtime = self.clock.now().nanoseconds
            self.stages += 1
            if self.stages > 2:
                self.stages = 0
            self.get_logger().info(f"stages: {self.stages}")
        if self.stages == 0:
            self.goal_joint_angle[0] = 0.0
            self.goal_joint_angle[1] = 0.0
            self.goal_joint_angle[2] = 0.0
            self.goal_joint_angle[3] = 0.0
            pathtime = 5.0
            self.send_goal_joint_space(pathtime)
        if self.stages == 1:
            self.goal_joint_angle[0] = 0.0
            self.goal_joint_angle[1] = -1.05
            self.goal_joint_angle[2] = 0.35
            self.goal_joint_angle[3] = 0.70
            pathtime = 5.0
            self.send_goal_joint_space(pathtime)

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
        except Exception as e:
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
