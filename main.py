import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# WLAN and MQTT configuration
WIFI_SSID = "YOUR_WIFI"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
MQTT_BROKER = "IP_ADDRESS_MQTT_BROKER"
MQTT_TOPIC_CONTROL = "MQTT_CHANNEL_FOR_COMMANDS"
MQTT_TOPIC_STATUS = "MQTT_CHANNEL_FOR_STATUS"
CLIENT_ID = "esp_relay_light"

RELAY_PIN = 2  # Pin for the relay
relay = Pin(RELAY_PIN, Pin.OUT)
relay_status = "off"

mqtt_client = None

# Connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    start_time = time.time()
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            if time.time() - start_time > 15:  # Timeout after 15 seconds
                print("Failed to connect to Wi-Fi. Rebooting...")
                machine.reset()
            time.sleep(1)
    print("Connected to Wi-Fi:", wlan.ifconfig())

# Receive message
def on_message(topic, msg):
    global relay_status
    try:
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
    except Exception as e:
        print(f"Error in message handling: {e}")

# Reconnect MQTT client if needed
def reconnect_mqtt():
    global mqtt_client
    while True:
        try:
            mqtt_client.connect()
            print("Reconnected to MQTT broker")
            mqtt_client.subscribe(MQTT_TOPIC_CONTROL)
            break
        except Exception as e:
            print(f"Reconnection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def main():
    global mqtt_client

    connect_to_wifi()

    # Create MQTT client
    mqtt_client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    mqtt_client.set_callback(on_message)
    try:
        mqtt_client.connect()
        print("Connected to MQTT broker")
        mqtt_client.subscribe(MQTT_TOPIC_CONTROL)
        print(f"Subscribed to: {MQTT_TOPIC_CONTROL}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        reconnect_mqtt()

    # Main loop
    while True:
        try:
            mqtt_client.wait_msg()  # Wait for new messages
        except OSError as e:
            print(f"MQTT error: {e}. Reconnecting...")
            reconnect_mqtt()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}. Restarting...")
        machine.reset()
