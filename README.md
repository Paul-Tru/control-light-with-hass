# Control a light using Home Assistant
control a relay using mqtt

## Requirements
1. Home Assistant [Installation](https://www.home-assistant.io/installation/)
2. Mosquitto Broker [Installation](https://mosquitto.org/download/)
3. ESP8266 (flashed with micropython)
4. A way to connect to the ESP (e.g. MicroPython Tools in PyCharm or PyMakr in VSCode)
5. Relay
6. A lamp or another device you want to control

## Installation

### Connect to Home Assistant
1. Go to `Settings` > `Devices & Services` > `Helper` > `Create Helper`
2. Search for a switch and give it a name (like `relay light`) and a symbol (like `mdi:lightbulb`)
3. Go back to `Automations & Scenes` and create a new automation
4. Click on the three periods in the top right and switch the view to `Edit as YAML` and Copy and Paste the following code in there:
   ```
   alias: YOUR_NAME
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
   ```
    And change the variables written in capital into the names you want to use#
5. Now go to the `Dashboard` and edit it. `Add card` > `Chose by entity`, than search for `input_boolean` and select your created switch

 ### Write the program to the ESP
  1. Connect your ESP to your computer via USB
  2. Open your code editor and connect to it

     For Visual Studio Code:
        1. Install the plugin `PyMakr` (Search in the extensions tab)
        2. You should now see a device in the pymakr tab. Hover on it and click on `Open in file explorer`
        3. Move `main.py` in the serial folder and change the capital variables so they work for you
        4. Go back to pymakr and click on `Create terminal`, then on the console in the bottom right
        5. Press `ctrl + d` to run main.py

     For PyCharm:
        1. Install `MicroPython Tools` (`Settings` > `Plugins...` > `Marketplace`)
        2. Click on the M in the bottom left, than `Change settings` > `Enable MicoPython Support`
        3. Close the window by clicking `OK` and install the missing Python packages (`Install...`)
        4. After it finished, press the dropdown menu (e.g. `COM3`) to connect to the esp
        5. Than press `REPL` and `ctrl + d` to run main.py
  3. To test, press the button in the Home Assistant Dashboard. The built-in LED should be turning on and off
  4. When you are sure the program is running stable, you can connect the esp to the relay and the lamp and install it wherever you want

