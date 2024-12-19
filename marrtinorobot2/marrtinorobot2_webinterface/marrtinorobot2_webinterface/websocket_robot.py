#!/usr/bin/env python3

import os
import time
from datetime import datetime
from threading import Thread
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

from robot_cmd_ros import RobotCmdROS

# Global variables
websocket_server = None  # WebSocket handler
run = True  # Main loop run flag
server_port = 9913  # Web server port
code = None
status = "Idle"  # Global robot status
list_ws = []
logdir = os.getenv('HOME') + '/log/'  # Directory for writing log files (programs, images,...)

class MyWebSocketServer(tornado.websocket.WebSocketHandler):
    def open(self):
        global list_ws
        self.client_ip = self.request.remote_ip
        print(f'New connection from {self.client_ip}')
        list_ws.append(self)
        print(f'Num connected clients: {len(list_ws)}')

    def on_message(self, message):
        global code, status
        if message == 'stop':
            print('Stop code and robot')
            if status != 'Idle':
                status = 'Stop'
            robot.stop()
        elif message.startswith('event'):
            print(f'Received event {message}')
        else:
            print('Code received')
            save_program(message)
            if status == 'Idle':
                run_code(message)
            else:
                print('Program running. This code is discarded.')
                self.write_message('Program running. This code is discarded.')

    def on_close(self):
        global list_ws
        print(f'Connection closed from {self.client_ip}')
        list_ws.remove(self)
        print(f'Num connected clients: {len(list_ws)}')

    def check_origin(self, origin):
        return True

def display(text):
    global list_ws
    for ws in list_ws:
        try:
            ws.write_message(f'display {text}')
        except tornado.websocket.WebSocketClosedError:
            print('Cannot write to closed WebSocket')

def main_loop():
    global run, status
    while run:
        time.sleep(1)
        for ws in list_ws:
            try:
                ws.write_message(status)
            except tornado.websocket.WebSocketClosedError:
                pass

fncode_running = False

def deffunctioncode(code):
    r = "def fncode():\n"
    r += "  robot.begin()\n"
    for line in code.splitlines():
        if not line.strip().startswith(('begin', 'end')):
            r += f"  {line}\n"
    r += "  robot.end()\n"
    return r

def fncodeexcept():
    global fncode_running
    fncode_running = True
    try:
        fncode()
    except Exception as e:
        print(f"CODE EXECUTION ERROR: {e}")
        display(str(e))
    fncode_running = False

def exec_thread(code):
    global fncode_running
    fncodestr = deffunctioncode(code)
    try:
        exec(fncodestr, globals())
    except Exception as e:
        print(f"FN CODE DEFINITION ERROR: {e}")
        display(str(e))
        return

    thread = Thread(target=fncodeexcept)
    thread.start()
    while fncode_running and status != "Stop":
        time.sleep(0.5)
    thread.join()

def save_program(code):
    try:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(logdir, f'{timestamp}.prg')
        with open(filename, 'w') as f:
            f.write(code)
    except Exception as e:
        print(f"ERROR saving program: {e}")

def run_code(code):
    global status
    if not code:
        return
    print("Executing code:")
    print(code)
    status = "Executing program"
    exec_thread(code)
    status = "Idle"

if __name__ == "__main__":
    os.makedirs(logdir, exist_ok=True)

    # Robot initialization
    rclpy.init()
    robot = RobotCmdROS()
    robot.begin()

    # Start WebSocket server
    application = tornado.web.Application([(r'/websocketserver', MyWebSocketServer)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(server_port)
    print(f"WebSocket server listening on port {server_port}")

    main_thread = Thread(target=main_loop)
    main_thread.start()

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("Keyboard interrupt, shutting down")

    # Cleanup
    robot.end()
    run = False
    main_thread.join()
    print("Web server and robot control stopped")
    rclpy.shutdown()
