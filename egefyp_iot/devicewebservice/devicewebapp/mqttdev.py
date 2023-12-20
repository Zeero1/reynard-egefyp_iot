import paho.mqtt.client as mqtt
from datetime import datetime as alert_time


global gdata1
global gdata2
gdata1=0.0
gdata2="Normal"

# Set this variable to True to enable MQTT connection, or False to run without MQTT
enable_mqtt = False


def on_connect(client, userdata, flags, rc):
    client.subscribe("test/#")
    #client.subscribe("test/sens1")

def on_message(client, userdata, msg):
    # Do something
    global gdata1
    global gdata2

    #print( msg.topic, msg.payload)
    print("Message Received: {},{}\n".format(msg.topic, msg.payload.decode("utf-8")))
    if msg.topic == "test/temp1":
        gdata1=str(msg.payload.decode("utf-8"))
        print("message temp1: {}".format(gdata1))

def clientconn():
    global client
    client = mqtt.Client("hostname1")
    client.on_connect = on_connect
    client.on_message = on_message

    if enable_mqtt:
        client.connect("192.168.23.1", 1883, 60)

def xdata():
    global gdata1
    data1=gdata1
    print("print data1:{}".format(data1))
    return data1

def ydata():
    global gdata2
    data2=gdata2
    print("print data2:{}".format(data2))
    return data2

def motor_on(activ_val):
    if client:
        if enable_mqtt and client:
            if int(activ_val) == 1:
                client.publish("eg281s-mqtt","{}".format(activ_val),qos=1)
                client.publish("test/motoron","{}".format(activ_val),qos=1)
                print("Fan turned ON")
            elif int(activ_val) == 0:
                client.publish("eg281s-mqtt","{}".format(activ_val),qos=1)
                client.publish("test/motoron","{}".format(activ_val),qos=1)
                print("Fan turned OFF")
    else:
        print("MQTT is not enabled or Client Not Connected!!")

if __name__ == '__main__':
    clientconn()

    if enable_mqtt:
        client.loop_forever()
    else:
        print("MQTT is disabled. Running locally without connecting to MQTT.")

"""
The first line imports the library functions for MQTT.

The callback functions
    on_connect - automatically called by the client upon connection to the broker
    on_message - automatically called upon receiving a message

The on_connect function prints the result of the connection attempt, and performs the subscription.
Note that subscribe happens only after the client is connected to the broker.

The on_message function prints the received message when it comes in, as well as the topic it was published under.

Body of the code:
1. Instantiate a client object with the client ID.
2. Define the callback functions to use upon connection and upon message receipt.
3. Connect to an MQTT broker at i.e. m2m.eclipse.org or a local broker: 102.168.20.1, on port 1883 (the default MQTT port)
   with a keepalive of 60 seconds (this is how often the client pings the broker to keep the connection alive).
4. The last line starts a network daemon that runs in the background and handles data transactions and messages, as well as keeping the socket open, until the script ends.
   In this case it never ends - loop_forever() unless the script is interrupted with a break command.
"""
