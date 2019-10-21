from mqtt import MQTTManager
from aiy.board import Board, Led
import aiy.voice.tts

class Talk2Soul:
    def __init__(self) -> None:
        super().__init__()
        self.board = Board()  # R pi aiy kit
        self.bulb_address = "172.30.1.15"
        self.led = Led
        self.mqtt_manager = MQTTManager(self.board, self.bulb_address, self.led)
        self.mqtt_manager.run()

    def button_handler(self):
        self.board.button.wait_for_press()
        print('ON')
        self.board.led.state = Led.ON
        self.board.button.wait_for_release()
        print('OFF')
        self.board.led.state = Led.OFF


def main():
    t2s = Talk2Soul()

    print('LED is ON while button is pressed (Ctrl-C for exit).')
    while True:
        t2s.button_handler()


if __name__ == '__main__':
    main()
