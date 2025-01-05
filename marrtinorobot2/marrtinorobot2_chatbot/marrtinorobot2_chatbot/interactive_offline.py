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
#
#! /usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import requests
import os
import random
import json

SERVER_ADDRESS = '10.3.1.1'
SERVER_PORT = 9000
myurl = 'http://10.3.1.1:5500/bot'

IN_TOPIC = "/social/face_nroface"
TOPIC_asr = "/social/asr"
TOPIC_gesture = "/social/gesture"
TOPIC_emotion = "social/emotion"
TOPIC_speech = "/speech/to_speak"
IN_TOPIC_speechstatus = "/speech/status"

class InteractiveNode(Node):
    def __init__(self):
        super().__init__('interactive_node')

        self.tracking = False
        self.asr_request = ""
        self.stspeech = ""
        self.mylanguage = "it"

        self.gesture_pub = self.create_publisher(String, TOPIC_gesture, 10)
        self.emotion_pub = self.create_publisher(String, TOPIC_emotion, 10)
        self.speech_pub = self.create_publisher(String, TOPIC_speech, 10)

        self.create_subscription(String, TOPIC_asr, self.callback_asr, 10)
        self.create_subscription(String, IN_TOPIC_speechstatus, self.callback_speechstatus, 10)

        self.say("Ciao sono Martina", self.mylanguage)
        self.say("Mi raccomando chiamami per nome quando ti rivolgi a me", self.mylanguage)
        self.emotion("startblinking")
        self.gesture("gesture")

    def say(self, msg, language):
        self.get_logger().info(f"Speech: {msg}")
        self.speech_pub.publish(String(data=msg))

    def emotion(self, msg):
        self.get_logger().info(f"Emotion: {msg}")
        self.emotion_pub.publish(String(data=msg))

    def gesture(self, msg):
        self.get_logger().info(f"Gesture: {msg}")
        self.gesture_pub.publish(String(data=msg))

    def bot(self, msg):
        payload = {'query': msg}
        self.get_logger().info(f"Query: {msg}")
        try:
            response = requests.get(url=myurl, params=payload)
            return response.content.decode('utf-8')
        except requests.exceptions.RequestException as e:
            self.get_logger().error(f"Bot request failed: {e}")
            return "Non riesco a rispondere al momento."

    def callback_asr(self, msg):
        myasr = msg.data
        if self.stspeech == "STOP":
            self.asr_request = myasr
            self.request(self.asr_request)
            self.get_logger().info(f"ASR Request: {self.asr_request}")

    def callback_speechstatus(self, msg):
        self.stspeech = msg.data
        if self.stspeech == 'STOP':
            self.emotion("normal")
        elif self.stspeech == 'START':
            self.emotion("speak")
        self.get_logger().info(f"Speech Status: {self.stspeech}")

    def request(self, myrequest):
        if myrequest != "":
            keyword = "martina"
            if myrequest.lower().startswith(keyword):
                mycommand = myrequest[len(keyword):].strip().lower()
                self.get_logger().info(f"Command: {mycommand}")
                
                if mycommand in ["parla inglese", "speak english"]:
                    self.mylanguage = "en"
                    self.say("I speak English now", self.mylanguage)
                elif mycommand in ["parla italiano", "speak italian"]:
                    self.mylanguage = "it"
                    self.say("Adesso parlo italiano", self.mylanguage)
                elif mycommand in ["alza le braccia", "raise your arms"]:
                    self.gesture("up")
                elif mycommand in ["saluta", "say hello"]:
                    self.gesture("hello")
                elif mycommand in ["abbassa le braccia", "lower your arms"]:
                    self.gesture("down")
                elif mycommand in ["spengiti", "spegniti", "arresta il sistema"]:
                    os.system("sudo halt")
                else:
                    answer = self.bot(mycommand)
                    self.say(answer, self.mylanguage)

        if myrequest in ["stop", "fine"]:
            self.say("Ci vediamo alla prossima", self.mylanguage)


def main(args=None):
    rclpy.init(args=args)
    node = InteractiveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down interactive node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
