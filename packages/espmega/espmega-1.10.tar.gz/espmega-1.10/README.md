# pyESPMega
This library provides a mean of communicating with the ESPMega Programmable Logic Controller through MQTT<br/>

## **Compatibility**
This library is compatible with:<br/>
- ESPMega R2.4 [2018] (Model e) with IoT FreedomOS v1.2+
- ESPMega R3.0 [2020] (All Model) with IoT Core LT OS V1.4
- ESPMega Plus R1.0 [2020] (All Model) with IoT Core LT+ OS V1.4
- ESPMega R4.0 [2023] (All Model) with IoT Core LT OS V2
- ESPMega PRO R2.0 [2020] (Model c) with IoT Core OS V1
- ESPMega PRO R3.3 [2023] (Model b,c) with IoT Core OS V2.2 (or above)

## **ESPMega Client Types**
There are two type of ESPMega client, ESPMega and ESPMega_standalone<br/>
### ESPMega
ESPMega class requires you to provide and maintain an MQTT connection
This class takes in a Paho-MQTT Client as an input argument<br/>
**Import and Initialization**
```
from espmega.espmega_r3 import ESPMega
plc = ESPMega("/basetopic", MQTT_CLIENT)
```
### ESPMega_standalone
ESPMega_standalone create and maintain the required mqtt connection for you.
**Import and Initialization**
```
from espmega.espmega_r3 import ESPMega_standalone as ESPMega
plc = ESPMega("/basetopic", "MQTT_SERVER", MQTT_PORT)
```
## **ESPMega Client Functions**
- `digital_read(pin: int) -> bool`: Reads the digital value from the specified pin.
- `digital_write(pin: int, state: bool) -> None`: Sets the digital state of a pin.
- `analog_write(pin: int, state: bool, value: int)`: Writes an analog value to the specified pin.
- `adc_read(pin: int) -> int`: Reads the value from the ADC pin.
- `dac_write(pin: int, state: bool, value: int)`: Writes the state and value to the DAC pin.
- `enable_adc(pin: int)`: Enables the ADC (Analog-to-Digital Converter) for the specified pin.
- `disable_adc(pin: int)`: Disable the ADC (Analog-to-Digital Converter) for the specified pin.
- `set_ac_mode(mode: str)`: Sets the mode of the air conditioner.
- `set_ac_temperature(temperature: int)`: Sets the temperature of the air conditioner.
- `set_ac_fan_speed(fan_speed: str)`: Sets the fan speed of the air conditioner.
- `get_ac_mode()`: Returns the current AC mode.
- `get_ac_temperature()`: Returns the current temperature of the air conditioning system.
- `get_ac_fan_speed()`: Get the current fan speed of the air conditioner.
- `read_room_temperature()`: Reads and returns the room temperature.
- `read_humidity()`: Reads and returns the humidity value from the humidity buffer.
- `send_infrared(code: dict)`: Sends an infrared code.
- `request_state_update()`: Update all cached states.
- `handle_message(client: pahomqtt.Client, data, message: pahomqtt.MQTTMessage)`: Handles incoming MQTT messages.
- `get_input_buffer()`: Return all states of the input pins as a list.
- `get_pwm_state(pin: int)`: Return the state of the specified PWM pin.
- `get_pwm_value(pin: int)`: Return the value of the specified PWM pin.
- `get_pwm_state_buffer()`: Return all states of the PWM pins as a list.
- `get_pwm_value_buffer()`: Return all values of the PWM pins as a list.