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
# file : speech-interface.py
#! /usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests

# Indirizzo del server Flask del chatbot
CHATBOT_URL = "http://localhost:5500/get"

class SayNode(Node):
    def __init__(self):
        super().__init__("say_node")
        self.subscription = self.create_subscription(
            String,
            "/say",
            self.listener_callback,
            10
        )
        self.get_logger().info("Listening on /say...")

    def listener_callback(self, msg: String):
        user_message = msg.data.strip()
        self.get_logger().info(f"Received message: '{user_message}'")

        # Invia la richiesta al chatbot Flask
        try:
            response = requests.get(CHATBOT_URL, params={"msg": user_message})
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "No response")
                self.get_logger().info(f"Chatbot says: {bot_response}")
            else:
                self.get_logger().error(f"Error: {response.status_code}")
        except requests.RequestException as e:
            self.get_logger().error(f"Request failed: {e}")

def main(args=None):
    rclpy.init(args=args)
    say_node = SayNode()
    rclpy.spin(say_node)
    say_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
