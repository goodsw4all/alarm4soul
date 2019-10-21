from google_speech import Speech
import paho.mqtt.client as mqtt
from yeelight import Bulb

HOST_ADDRESS = '127.0.0.1'
TOPIC_TALK = 'home/talk2soul'
TOPIC_BULB1_COMMAND = 'home/bulb/soul_bed/command'
TOPIC_BULB1_STATUS = 'home/bulb/soul_bed/status'

class MQTTManager(mqtt.Client):
    def __init__(self, board, bulb_address, led,
                 client_id="",
                 clean_session=True,
                 userdata=None,
                 protocol=mqtt.MQTTv311,
                 transport="tcp"):
        super().__init__(client_id, clean_session, userdata, protocol, transport)
        self.board = board
        self.bulb = Bulb(bulb_address, effect='smooth', duration=300)
        self.led = led

    def on_connect(self, mqttc, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.subscribe(TOPIC_TALK)
        self.subscribe(TOPIC_BULB1_COMMAND)
        print(self.bulb.get_properties())

    def on_message(self, mqttc, userdata, msg):
        print(msg.topic+" " + str(msg.qos)+" "+str(msg.payload))
        cmd = msg.payload.decode('utf-8')

        if msg.topic == TOPIC_TALK:
            print("Talk to Soul!!! " + cmd)
            lang = "ko"
            speech = Speech(cmd, lang)
            sox_effects = ("speed", "1.2")
            speech.play(sox_effects)

        elif msg.topic == TOPIC_BULB1_COMMAND:
            if cmd == "lighton":
                self.bulb.turn_on()
            elif cmd == "lightoff":
                self.bulb.turn_off()
            elif cmd.startswith("brightness"):
                args = cmd.split()
                print(args[1])
                self.bulb.set_brightness(int(args[1]))
            elif cmd.startswith("rgb"):
                args = cmd.split()
                r = int(args[1])
                g = int(args[2])
                b = int(args[3])
                print(r, g, b)
                self.bulb.set_rgb(r, g, b)
            elif cmd.startswith("hsv"):
                args = cmd.split()
                h = int(args[1])
                s = int(args[2])
                v = int(args[3])
                print(h, s, v)
                self.bulb.set_hsv(h, s, v)
            elif cmd.startswith("ct"):
                args = cmd.split()
                temp = int(args[1])

                self.bulb.set_color_temp(temp)
            elif cmd.startswith("status"):
                props = self.bulb.get_properties()
                for k, v in props.items():
                    print(k, ":", v)
                (rc, mid) = self.publish(TOPIC_BULB1_STATUS, str(props), qos=2)

    def on_publish(self, userdata, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, userdata, level, string):
        print(string)

    def run(self):
        self.username_pw_set('homeiot', 'homeiot0901')
        self.connect(host=HOST_ADDRESS, port=1883, keepalive=60)
        self.loop_start()




