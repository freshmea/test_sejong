import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Move_turtle(Node):
    def __init__(self):
        super().__init__('mturtle')
        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.create_timer(0.1, self.publisher)
        self.create_timer(1/60, self.update)
        self.speed = 0.0
        self.dir = 1.0

    def publisher(self):
        msg = Twist()
        msg.linear.x = self.speed
        msg.angular.z = self.dir
        self.pub.publish(msg)

    def update(self):
        # speed, dir 
        self.speed += 0.001 * self.dir
        if self.speed > 2:
            self.dir = -1.0
        elif self.speed < 0:
            self.dir = 1.0
        print(self.speed, self.dir)


def main():
    rclpy.init()
    node = Move_turtle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()