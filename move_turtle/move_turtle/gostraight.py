import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

MAX_LIN_VEL = 0.22
MAX_ANG_VEL = 2.84

class Move_straight(Node):
    def __init__(self):
        super().__init__('straight')
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.odometery_sub = self.create_subscription(Odometry, 'odom', self.odom_sub)
        self.create_timer(0.1, self.publisher)
        self.create_timer(1/60, self.update)
        self.speed = 0.0
        self.dir = 1.0
        self.origin_x = 0.0
        self.origin_y = 0.0

    def odom_sub(self, data):
        self.x = data.pose.pose.position.x
        self.y = data.pose.pose.position.y

    def straight(self, distance):
        self.origin_x = self.x
        self.origin_y = self.y
        
        while rclpy.ok():
            #publish
            pass
    
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
    node = Move_straight()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.destroy_node
        rclpy.shutdown()

if __name__ == '__main__':
    main()

# ------------------
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import sqrt

MAX_LIN_SPEED =  0.22
LIN_SPD = MAX_LIN_SPEED * 0.325

class TB3Pose2D(Node):

    def __init__(self):
        super().__init__('move_tb3')
        qos_profile = QoSProfile(depth=10)
        self.sub_ar_pose = self.create_subscription(
            Pose,               # topic type
            'tb3pose2d',        # topic name
            self.get_pose_cb,   # callback function
            qos_profile)
        self.pub = self.create_publisher(Twist, '/cmd_vel', qos_profile)        
        self.tb3pose  = Pose()  # for subscribe
        self.org = Pose()  # for store starting point
        
    def get_pose_cb(self, msg):
        # callback function to subscribe "/tb3pose" topic
        self.tb3pose = msg
        
    def update_org(self):
        # save current tb3pose.x, y to org.x, y when called this function
        self.org = self.tb3pose
        
    def elapsed_dist(self):
        # calcurate and return elapsed distance
        return sqrt(pow((self.tb3pose.x - self.org.x), 2) + pow((self.tb3pose.y - self.org.y), 2))
    
    def straight(self, distance):
        # forward or backward until elaped distance is equal to target distance
        tw = Twist()
        
        if distance >= 0:   # distance(+): forward
            tw.linear.x =  LIN_SPD
        else:               # distance(-): backward
            tw.linear.x = -LIN_SPD
        rclpy.spin_once(self)
        for i in range(10):
            self.update_org()   # update starting point
        print("start at (%s, %s)" %(round(self.org.x, 2), round(self.org.y, 2)))#,
        self.pub.publish(tw)    # start move
        
        while rclpy.ok():
            rclpy.spin_once(self)
            self.pub.publish(tw)
            print(self.elapsed_dist())
            print(self.tb3pose.x, self.tb3pose.y)
            if self.elapsed_dist() < abs(distance):
                pass
            else:                              
                break
        
        tw.linear.x = 0.0;    self.pub.publish(tw) # stop move
        print("stop  at (%s, %s)" %(round(self.tb3pose.x, 2), round(self.tb3pose.y, 2)))

def main(args=None):
    rclpy.init(args=args)
    node = TB3Pose2D()
    
    try:
        dist = float(input("input distance to straight(m): "))
        node.straight(dist)
        rclpy.spin(node)
                
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt(SIGINT)')
        
    finally:
        node.destroy_node()
        rclpy.shutdown()
    
            
if __name__ == '__main__':
    main()