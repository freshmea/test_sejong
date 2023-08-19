import rclpy
from rclpy.node import Node 
from std_srvs.srv import SetBool
import RPi.GPIO as g

class Gpio_led_server(Node):
    def __init__(self):
        super().__init__('gpioLedServer')
        self.srv = self.create_service(SetBool, 'gpio_led_server', self.gpio_led)
        g.setmode(g.BCM)
        g.setup(21, g.OUT)

    def gpio_led(self, request, response):
        self.get_logger().info(f'incomming data{request.data}')
        if request.data:
            g.output(21, True)
        else:
            g.output(21, False)
        response.success = True
        response.message = 'ok'
        return response

def main(args = None):
    rclpy.init(args = args)
    node = Gpio_led_server()
    try:
        rclpy.spin(node)
    except:
        g.cleanup()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main':
    main()
