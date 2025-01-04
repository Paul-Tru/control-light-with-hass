# Control a light using Home Assistant
control a relay using mqtt

## Requirements
1. Home Assistant [Installation](https://www.home-assistant.io/installation/)
2. Mosquitto Broker [Installation](https://mosquitto.org/download/)
3. ESP8266
4. A way to connect to the ESP (e.g. MicroPython Tools in PyCharm or PyMakr in VSCode)
5. Relay
6. A lamp or an other device you want to control

## Connect to Home Assistant
1. Go to "Settings"
2. Click on "Devices & Services"
3. Switch to the tab "Helper"
4. "Create Helper"
5. Search for a switch
6. Give it a name (like "Relay Light") and a symbol (like mdi:lightbuld)
7. Go back to "Automations & Scenes" and create a new automation
8. Click on the three periods and switch the view to "edit as YAML"
9. Copy Paste the following code in there:
  '''
  alias: Relay Light
  description: Turns on the relay based on the state from input_boolean.YOUR_SWITCH
  triggers:
    - entity_id: input_boolean.YOUR_SWITCH
      trigger: state
  actions:
    - data:
        topic: YOUR_MQTT_CONTROL_CHANNEL
        payload: "{{ states('input_boolean.YOUR_SWITCH') }}"
      action: mqtt.publish
  mode: single
  
  '''
  And change the variables written in capital into the names you want to use
