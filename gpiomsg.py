import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as g
import time

class Gpio_sub(Node):
    def __init__(self):
        super().__init__('gpio')
        self.servo_pin = 12 
        self.create_subscription(String, 'gpio_msg', self.sub, 10)
        g.setmode(g.BCM)
        g.setup(21, g.OUT)
        g.setup(self.servo_pin, g.OUT)
        self.pwm = g.PWM(self.servo_pin, 50)
        self.pwm.start(3.0)
        
    def sub(self, msg):
        self.get_logger().info(f'Recived message: {msg.data}')
        if msg.data == 'ledon':
            g.output(21, True)
        if msg.data == 'ledoff':
            g.output(21, False)
        if msg.data[:5] == 'servo':
            self.pwm.ChangeDutyCycle(float(msg.data[5:])/180*12.5)

def main():
    rclpy.init()
    node = Gpio_sub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('keyboard Interrupt!!')
    finally:
        node.pwm.stop()
        g.cleanup()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()