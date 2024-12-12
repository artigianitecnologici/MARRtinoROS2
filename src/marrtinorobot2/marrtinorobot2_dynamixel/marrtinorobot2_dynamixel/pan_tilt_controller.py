#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from dynamixel_sdk import *  # Libreria Dynamixel SDK
from std_msgs.msg import Float64  # Messaggio per i comandi di posizione


class DynamixelController(Node):
    def __init__(self):
        super().__init__('dynamixel_controller')

        # Inizializzazione della porta e del packet handler per Dynamixel
        self.port_handler = PortHandler('/dev/dynamixel')  # Porta seriale
        self.packet_handler = PacketHandler(1.0)         # Versione protocollo
        self.baudrate = 1000000
        self.pan_motor_id = 2
        self.tilt_motor_id = 1
        self.init_dynamixel()

        # Sottoscrittori per i comandi pan e tilt
        self.pan_subscriber = self.create_subscription(
            Float64, 'pan_controller/command', self.pan_callback, 10)
        self.tilt_subscriber = self.create_subscription(
            Float64, 'tilt_controller/command', self.tilt_callback, 10)

    def init_dynamixel(self):
        if self.port_handler.openPort():
            self.get_logger().info('Port opened successfully.')
        else:
            self.get_logger().error('Failed to open port.')

        if self.port_handler.setBaudRate(self.baudrate):
            self.get_logger().info('Baudrate set successfully.')
        else:
            self.get_logger().error('Failed to set baudrate.')

    def set_position(self, motor_id, position, speed):
        # Imposta la velocità di movimento (indirizzo 32)
        result_speed, error_speed = self.packet_handler.write2ByteTxRx(self.port_handler, motor_id, 32, speed)
        if result_speed != COMM_SUCCESS:
            self.get_logger().error(f'Failed to set speed: {self.packet_handler.getTxRxResult(result_speed)}')
        elif error_speed != 0:
            self.get_logger().error(f'Error occurred when setting speed: {self.packet_handler.getRxPacketError(error_speed)}')
        else:
            self.get_logger().info(f'Motor {motor_id} speed set to {speed}')

        # Imposta la posizione del servo (indirizzo 30)
        result_pos, error_pos = self.packet_handler.write2ByteTxRx(self.port_handler, motor_id, 30, int(position))
        if result_pos != COMM_SUCCESS:
            self.get_logger().error(f'Failed to set position: {self.packet_handler.getTxRxResult(result_pos)}')
        elif error_pos != 0:
            self.get_logger().error(f'Error occurred when setting position: {self.packet_handler.getRxPacketError(error_pos)}')
        else:
            self.get_logger().info(f'Motor {motor_id} moved to position {int(position)}')

    # Callback per il comando pan
    def pan_callback(self, msg):
        self.get_logger().info(f'Received pan command: {msg.data}')
        pan_position = msg.data  # Posizione da impostare per il motore Pan
        speed = 50  # Imposta la velocità del motore Pan
        self.set_position(self.pan_motor_id, pan_position, speed)

    # Callback per il comando tilt
    def tilt_callback(self, msg):
        self.get_logger().info(f'Received tilt command: {msg.data}')
        tilt_position = msg.data  # Posizione da impostare per il motore Tilt
        speed = 50  # Imposta la velocità del motore Tilt
        self.set_position(self.tilt_motor_id, tilt_position, speed)


def main(args=None):
    rclpy.init(args=args)

    # Inizializza il nodo DynamixelController
    controller = DynamixelController()
     # Imposta il motore pan a posizione 512 (centrale) e velocità 100
    controller.set_position(1, 512,40)
    # Imposta il motore tilt a posizione 512 (centrale) e velocità 200
    controller.set_position(2, 512, 40)

    # Esegui il nodo in modalità loop
    rclpy.spin(controller)

    # Spegni ROS 2 quando il nodo viene terminato
    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
