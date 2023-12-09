import paho.mqtt.client as pahomqtt
from time import sleep


class ESPMega:
    mqtt: pahomqtt.Client
    original_callback_func = None
    input_chnaged_cb = None
    input_buffer = [False]*16
    pwm_state_buffer = [False]*16
    pwm_value_buffer = [0]*16
    adc_buffer = [0]*8
    humidity_buffer: float = None
    room_temperature_buffer: float = None
    ac_mode_buffer: str = None
    ac_temperature_buffer: int = None
    ac_fan_speed_buffer: str = None
    avaliable: bool = False
    rapid_response_mode: bool = False

    def __init__(self, base_topic: str, mqtt: pahomqtt.Client, input_callback=None):
        self.mqtt = mqtt
        self.base_topic = base_topic
        self.mqtt.subscribe(f'{base_topic}/input/#')
        self.mqtt.subscribe(f'{base_topic}/ac/humidity')
        self.mqtt.subscribe(f'{base_topic}/ac/room_temperature')
        self.mqtt.subscribe(f'{base_topic}/ac/mode')
        self.mqtt.subscribe(f'{base_topic}/ac/temperature')
        self.mqtt.subscribe(f'{base_topic}/ac/fan_speed')
        self.mqtt.subscribe(f'{base_topic}/adc/#')
        self.mqtt.subscribe(f'{base_topic}/pwm/#')
        self.mqtt.subscribe(f'{base_topic}/ac/#')
        self.mqtt.subscribe(f'{base_topic}/availability')
        self.original_callback_func = self.mqtt.on_message
        self.mqtt.on_message = self.handle_message
        self.request_state_update()
        sleep(1)
        if (not self.avaliable):
            raise Exception(
                "ESPMega is not avaliable, please check the connection.")

    def enable_rapid_response_mode(self):
        """
        Enables rapid response mode.

        Returns:
            None
        """
        self.__check_availability()
        self.mqtt.publish(f'{self.base_topic}/rapid_response_mode', "on")
        self.rapid_response_mode = True

    def disable_rapid_response_mode(self):
        """
        Disables rapid response mode.

        Returns:
            None
        """
        self.__check_availability()
        self.mqtt.publish(f'{self.base_topic}/rapid_response_mode', "off")
        self.request_state_update()
        self.rapid_response_mode = False

    def digital_read(self, pin: int) -> bool:
        """
        Reads the digital value from the specified pin.

        Args:
            pin (int): The pin number to read from.

        Returns:
            bool: The digital value read from the pin.
        """
        self.__check_availability()
        return self.input_buffer[pin]

    def digital_write(self, pin: int, state: bool) -> None:
        """
        Sets the digital state of a pin.

        Args:
            pin (int): The pin number.
            state (bool): The desired state of the pin. True for HIGH, False for LOW.
        """
        self.__check_availability()
        if (state != self.pwm_state_buffer[pin]):
            self.mqtt.publish(
                f'{self.base_topic}/pwm/{"%02d"}/set/state' % pin, "on" if state else "off")
            if(self.rapid_response_mode):
                self.pwm_state_buffer[pin] = state
        if (self.rapid_response_mode):
            # In rapid response mode, set the value to 4095 for all case
            if (self.pwm_value_buffer[pin] != 4095):
                self.mqtt.publish(
                    f'{self.base_topic}/pwm/{"%02d"}/set/value' % pin, 4095)
                self.pwm_value_buffer[pin] = 4095
        else:
            if (self.pwm_value_buffer[pin] != (4095 if state else 0)):
                self.mqtt.publish(
                    f'{self.base_topic}/pwm/{"%02d"}/set/value' % pin, 4095 if state else 0)

    def analog_write(self, pin: int, state: bool, value: int):
        """
        Writes an analog value to the specified pin.

        Args:
            pin (int): The pin number.
            state (bool): The state of the pin (on/off).
            value (int): The analog value to write.

        Returns:
            None
        """
        self.__check_availability()
        if (state != self.pwm_state_buffer[pin]):
            self.mqtt.publish(
                f'{self.base_topic}/pwm/{"%02d"}/set/state' % pin, "on" if state else "off")
            if(self.rapid_response_mode):
                self.pwm_state_buffer[pin] = state
        if (value != self.pwm_value_buffer[pin]):
            self.mqtt.publish(
                f'{self.base_topic}/pwm/{"%02d"}/set/value' % pin, int(value))
            if(self.rapid_response_mode):
                self.pwm_value_buffer[pin] = value

    def adc_read(self, pin: int) -> int:
        """
        Reads the value from the ADC pin.

        Parameters:
            pin (int): The pin number to read from.

        Returns:
            int: The value read from the ADC pin.

        Note:
            The value will only update if the ADC is enabled.
        """
        self.__check_availability()
        return self.adc_buffer[pin]

    def dac_write(self, pin: int, state: bool, value: int):
        """
        Writes the state and value to the DAC pin.

        Args:
            pin (int): The DAC pin number.
            state (bool): The state of the DAC pin (True for on, False for off).
            value (int): The value to be written to the DAC pin.

        Returns:
            None
        """
        self.__check_availability()
        self.mqtt.publish(
            f'{self.base_topic}/dac/{"%02d"}/set/state' % pin, "on" if state else "off")
        self.mqtt.publish(
            f'{self.base_topic}/dac/{"%02d"}/set/value' % pin, int(value))

    def enable_adc(self, pin: int):
        """
        Enables the ADC (Analog-to-Digital Converter) for the specified pin.

        Args:
            pin (int): The pin number to enable ADC for.

        Returns:
            None
        """
        self.__check_availability()
        print(f'{self.base_topic}/adc/{"%02d"}/set/state' % pin)
        self.mqtt.publish(
            f'{self.base_topic}/adc/{"%02d"}/set/state' % pin, "on")

    def disable_adc(self, pin: int):
        """
        Disable the ADC (Analog-to-Digital Converter) for the specified pin.

        Args:
            pin (int): The pin number to disable the ADC for.

        Returns:
            None
        """
        self.__check_availability()
        self.mqtt.publish(
            f'{self.base_topic}/adc/{"%02d"}/set/state' % pin, "off")

    def set_ac_mode(self, mode: str):
        """
        Sets the mode of the air conditioner.

        Args:
            mode (str): The mode to set the air conditioner to.

        Returns:
            None
        """
        self.__check_availability()
        self.mqtt.publish(f'{self.base_topic}/ac/set/mode', mode)

    def set_ac_temperature(self, temperature: int):
        """
        Sets the temperature of the air conditioner.

        Args:
            temperature (int): The desired temperature to set.

        Returns:
            None
        """
        self.__check_availability()
        self.mqtt.publish(
            f'{self.base_topic}/ac/set/temperature', str(temperature))

    def set_ac_fan_speed(self, fan_speed: str):
        """
        Sets the fan speed of the air conditioner.

        Args:
            fan_speed (str): The desired fan speed.

        Returns:
            None
        """
        self.__check_availability()
        self.mqtt.publish(f'{self.base_topic}/ac/set/fan_speed', fan_speed)

    def get_ac_mode(self):
        """
        Returns the current AC mode.

        Returns:
            str: The current AC mode.
        """
        self.__check_availability()
        return self.ac_mode_buffer

    def get_ac_temperature(self):
        """
        Returns the current temperature of the air conditioning system.
        """
        self.__check_availability()
        return self.ac_temperature_buffer

    def get_ac_fan_speed(self):
        """
        Get the current fan speed of the air conditioner.

        Returns:
            int: The fan speed value.
        """
        self.__check_availability()
        return self.ac_fan_speed_buffer

    def read_room_temperature(self):
        """
        Reads and returns the room temperature.

        Returns:
            float: The room temperature.
        """
        self.__check_availability()
        return self.room_temperature_buffer

    def read_humidity(self):
        """
        Reads and returns the humidity value from the humidity buffer.

        Returns:
            The humidity value from the humidity buffer.
        """
        self.__check_availability()
        return self.humidity_buffer

    def send_infrared(self, code: list):
        """
        Sends an infrared code.

        Args:
            code (list): The infrared code to send.

        Returns:
            None
        """
        self.__check_availability()
        payload = ','.join(str(num) for num in code)
        self.mqtt.publish(f'{self.base_topic}/ir/send', payload)

    def request_state_update(self):
        """
        Update all cached states.
        """
        self.mqtt.publish(f'{self.base_topic}/requeststate', "req")

    def handle_message(self, client: pahomqtt.Client, data, message: pahomqtt.MQTTMessage):
        if (message.topic.startswith(self.base_topic+"/input/")):
            id = int(message.topic[len(self.base_topic)+7:len(message.topic)])
            state = bool(int(message.payload))
            if self.input_chnaged_cb != None:
                self.input_chnaged_cb(id, state)
            self.input_buffer[id] = state
        elif (message.topic.startswith(self.base_topic+"/adc/") and message.topic.endswith("/report")):
            id = int(
                message.topic[len(self.base_topic)+5:len(message.topic)+6])
            self.adc_buffer[id] = int(message.payload)
        elif (message.topic == (f'{self.base_topic}/ac/humidity')):
            if message.payload != (b'ERROR'):
                self.humidity_buffer = float(message.payload)
        elif (message.topic == (f'{self.base_topic}/ac/room_temperature')):
            if message.payload != (b'ERROR'):
                self.room_temperature_buffer = float(message.payload)
        elif (message.topic == (f'{self.base_topic}/ac/mode')):
            self.ac_mode_buffer = message.payload.decode("utf-8")
        elif (message.topic == (f'{self.base_topic}/ac/temperature')):
            self.ac_temperature_buffer = int(message.payload)
        elif (message.topic == (f'{self.base_topic}/ac/fan_speed')):
            self.ac_fan_speed_buffer = message.payload.decode("utf-8")
        elif (message.topic.startswith(f'{self.base_topic}/pwm/') and message.topic.endswith("/state") and len(message.topic) == len(self.base_topic)+13):
            pwm_id = int(
                message.topic[len(self.base_topic)+5:len(self.base_topic)+7])
            if (message.payload == b'on'):
                self.pwm_state_buffer[pwm_id] = True
            elif (message.payload == b'off'):
                self.pwm_state_buffer[pwm_id] = False
        elif (message.topic.startswith(f'{self.base_topic}/pwm/') and message.topic.endswith("/value") and len(message.topic) == len(self.base_topic)+13):
            pwm_id = int(
                message.topic[len(self.base_topic)+5:len(self.base_topic)+7])
            self.pwm_value_buffer[pwm_id] = int(
                message.payload.decode("utf-8"))
        elif (message.topic == (f'{self.base_topic}/availability')):
            if (message.payload == b'online'):
                self.avaliable = True
            elif (message.payload == b'offline'):
                self.avaliable = False
        if (self.original_callback_func!= None):
            self.original_callback_func(client, data, message)

    def get_input_buffer(self):
        """
          Return all states of the input pins as a list.
        """
        self.__check_availability()
        return self.input_buffer

    def get_pwm_state(self, pin: int):
        """
          Return the state of the specified PWM pin.
        """
        self.__check_availability()
        return self.pwm_state_buffer[pin]

    def get_pwm_value(self, pin: int):
        """
          Return the value of the specified PWM pin.
        """
        self.__check_availability()
        return self.pwm_value_buffer[pin]

    def get_pwm_state_buffer(self):
        """
          Return all states of the PWM pins as a list.
        """
        self.__check_availability()
        return self.pwm_state_buffer

    def get_pwm_value_buffer(self):
        """
          Return all values of the PWM pins as a list.
        """
        self.__check_availability()
        return self.pwm_value_buffer

    def is_available(self):
        """
          Return the availability of the ESPMega.
        """
        return self.avaliable

    def __check_availability(self):
        if (not self.avaliable):
            raise Exception(
                "ESPMega is not avaliable, please check the connection.")


class ESPMega_standalone(ESPMega):
    def __init__(self, base_topic: str, mqtt_server: str, mqtt_port: int, mqtt_use_auth: bool = False,
                 mqtt_username: str = None, mqtt_password: str = None,
                 input_callback=None):
        self.mqtt = pahomqtt.Client()
        if (mqtt_use_auth):
            self.mqtt.username_pw_set(mqtt_username, mqtt_password)
        self.mqtt.connect(host=mqtt_server, port=mqtt_port, keepalive=60)
        self.mqtt.loop_start()
        super().__init__(base_topic=base_topic, mqtt=self.mqtt, input_callback=input_callback)


class ESPMega_slave(ESPMega):
    def __init__(self, base_topic: str, master: ESPMega_standalone, input_callback=None):
        super().__init__(base_topic, master.mqtt, input_callback=input_callback)