import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess

class CommandExecutorNode(Node):
    def __init__(self):
        super().__init__('command_executor')
        self.subscription = self.create_subscription(
            String,
            'shell_command',
            self.execute_command_callback,
            10)
        self.publisher = self.create_publisher(String, 'command_output', 10)

    def execute_command_callback(self, msg):
        command = msg.data
        self.get_logger().info(f'Received command: {command}')
        
        try:
            # Esegue il comando shell
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr
        except Exception as e:
            output = f'Error: {str(e)}'
        
        # Pubblica l'output del comando
        output_msg = String()
        output_msg.data = output
        self.publisher.publish(output_msg)
        self.get_logger().info(f'Command output: {output}')

def main(args=None):
    rclpy.init(args=args)
    node = CommandExecutorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
