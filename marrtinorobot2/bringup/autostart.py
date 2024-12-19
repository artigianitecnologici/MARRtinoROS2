# Copyright 2025 robotics-3d.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Ferrarini Fabio
# Email : ferrarini09@gmail.com

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import subprocess
import json
import time

class CommandExecutorNode(Node):
    def __init__(self):
        super().__init__('autostart')
        self.publisher = self.create_publisher(String, 'command_output', 10)
        self.get_logger().info('Autostart Node started.')

        # Percorso al file JSON
        json_path = '~/src/marrtinorobot2/marrtinorobot2_webinterface/www/bringup/commands.json'

        # Carica il file JSON
        try:
            with open(json_path, 'r') as file:
                self.commands = json.load(file)
        except Exception as e:
            self.get_logger().error(f'Error loading JSON file from {json_path}: {str(e)}')
            self.commands = []

        # Esegue i comandi con "selected": true
        self.execute_selected_commands()

    def execute_selected_commands(self):
        for command_entry in self.commands:
            if command_entry.get('selected', False):
                start_command = command_entry.get('startCommand', '')
                title = command_entry.get('title', 'Unknown')
                
                if start_command:
                    self.get_logger().info(f'Executing startCommand for {title}: {start_command}')
                    try:
                        result = subprocess.run(start_command, shell=True, capture_output=True, text=True)
                        output = result.stdout + result.stderr
                    except Exception as e:
                        output = f'Error executing {title}: {str(e)}'

                    # Pubblica l'output del comando
                    output_msg = String()
                    output_msg.data = f'[{title}] {output}'
                    self.publisher.publish(output_msg)
                    self.get_logger().info(f'Output for {title}: {output}')

                    # Pausa tra un comando e l'altro
                    time.sleep(2)


def main(args=None):
    rclpy.init(args=args)
    node = CommandExecutorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
