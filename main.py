import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# WLAN and MQTT configuartion
WIFI_SSID = "YOUR_WIFI"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
MQTT_BROKER = "IP_ADRESS_MQTT_BROKER"
MQTT_TOPIC_CONTROL = "MQTT_CHANNEL_FOR_COMMANDS"
MQTT_TOPIC_STATUS = "MQTT_CHANNEL_FOR_STATUS"
CLIENT_ID = "esp_relay_light"

RELAY_PIN = 2 # Pin for the relay
relay = Pin(RELAY_PIN, Pin.OUT)
relay_status = "off"

mqtt_client = None

# Connect wifi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected:", wlan.ifconfig())

# Recive message
def on_message(topic, msg):
    global relay_status
    if topic.decode() == MQTT_TOPIC_CONTROL:
        command = msg.decode()
        if command == "on":
            relay.on()
            relay_status = "on"
            print("Relay turned on")
        elif command == "off":
            relay.off()
            relay_status = "off"
            print("Relay turned off")

        # Publish status
        mqtt_client.publish(MQTT_TOPIC_STATUS, relay_status)

def main():
    global mqtt_client

    connect_to_wifi()

    # Create MQTT-client
    mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    mqtt_client.set_callback(on_message)
    mqtt_client.connect()
    print("Connected to MQTT-Broker")
    mqtt_client.subscribe(MQTT_TOPIC_CONTROL)
    print(f"Subscribed: {MQTT_TOPIC_CONTROL}")

    # Loop for reciving messages and publishing status 
    while True:
        mqtt_client.wait_msg()  # Waiting for new messages
        mqtt_client.publish(MQTT_TOPIC_STATUS, relay_status)  # send status
        print(f"Send status: {relay_status}")
      
if __name__ == "__main__":
    main()
