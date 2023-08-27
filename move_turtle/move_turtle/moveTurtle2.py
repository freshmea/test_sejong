import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

MAX_LIN_VEL = 0.22
MAX_ANG_VEL = 2.84
class Move_turtle(Node):
    def __init__(self):
        super().__init__('mturtle')
        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.pub2 = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
        self.create_timer(0.1, self.publisher)
        self.create_timer(0.1, self.publisher2)
        self.create_timer(1/60, self.update)
        self.speed = 0.0
        self.dir = 1.0

    def publisher(self):
        msg = Twist()
        msg.linear.x = self.speed
        msg.angular.z = self.dir
        msg = self.restrain(msg)
        self.pub.publish(msg)
        
    def publisher2(self):
        msg = Twist()
        msg.linear.x = self.speed
        msg.angular.z = -self.dir
        msg = self.restrain(msg)
        self.pub2.publish(msg)

    def update(self):
        # speed, dir 
        # sec, nano = self.get_clock().now().seconds_nanoseconds
        self.speed += 0.01 * self.dir
        if self.speed > 2:
            self.dir = -1.0
        elif self.speed < 0:
            self.dir = 1.0
        print(self.speed, self.dir)
        
    def restrain(self, msg):
        if msg.linear.x < - MAX_LIN_VEL:
            msg.linear.x = - MAX_LIN_VEL
        elif msg.linear.x > MAX_LIN_VEL:
            msg.linear.x = MAX_LIN_VEL
        if msg.angular.z < - MAX_ANG_VEL:
            msg.angular.z = - MAX_ANG_VEL
        elif msg.angular.z > MAX_ANG_VEL:
            msg.angular.z = MAX_ANG_VEL
        return msg


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