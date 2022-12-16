import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    global loop_flag
    print("Connected with result code "+str(rc))
    loop_flag=0
    client.publish("pi", "sup on connect")
    client.subscribe("test")
    client.subscribe("matt")
    client.subscribe("caleb")
    client.subscribe("ben")


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))
    data = json.loads(msg.payload.decode("utf-8"))
    regs = data["inregions"]
    print(regs)
    if len(regs) > 1  and regs[0] == 'School':
        print(regs[1])
    else:
        print(regs[0])





def main():
    try:
        client = mqtt.Client("pi")
        client.on_connect = on_connect
        client.on_message = on_message
        client.username_pw_set(username="xoemllsy", password="hdgazSRFNst3")
        print("connecting...")
        client.connect("farmer.cloudmqtt.com", port=14479)
        client.loop_forever()
    except KeyboardInterrupt:
        print("bye!")
        exit(1)

if __name__ == '__main__':
    main()