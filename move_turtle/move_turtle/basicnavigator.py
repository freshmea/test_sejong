import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
import RPi.GPIO as g


class Gpio_led_server(Node):
    """
    A class representing a GPIO LED server.

    This class creates a ROS service that can be used to control an LED connected
    to a GPIO pin on a Raspberry Pi.

    """
    
    def __init__(self):
        """
        Initializes the GPIO LED server node.
        This method sets up a ROS service that can be used to control an LED
        connected to GPIO pin 21 on a Raspberry Pi.
        """
        super().__init__('gpioLedServer')
        self.srv = self.create_service(SetBool, 'gpio_led_server', self.gpio_led)
        g.setmode(g.BCM)
        g.setup(21, g.OUT)

    def gpio_led(self, request, response):
        """_summary_
        Args:
            request (_type_): _description_
            response (_type_): _description_

        Returns:
            _type_: _description_
        """
        self.get_logger().info(f'incomming data{request.data}')
        if request.data:
            g.output(21, True)
        else:
            g.output(21, False)
        response.success = True
        response.message = 'ok'
        return response


def main(args=None):
    """_summary_

    Args:
        args (_type_, optional): _description_. Defaults to None.
    """
    rclpy.init(args=args)
    node = Gpio_led_server()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        g.cleanup()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
