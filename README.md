# ***Gas Leak and Smoke Detection using IOT***

### Features
- Real-Time update on Adafruit Server.
- Uses Micropython to Code the Program.
- Can send SMS to the Registered mobile number if Gas Leak detected.
- Able to Monitier device over Internet.

### Components :
##### Flame Sensor :
- The [Flame Sensor][Flame] Module can detect flames in the 760 – 1100 nanometer wavelength range. Small flames like a lighter flame can be detected at roughly 0.8m. The detection angle is roughly 60 degrees and the sensor is particularly sensitive to the flame spectrum.
- An on-board LM393 op-amp is used as a comparator to adjust the sensitivity level. The sensor has a digital and analog output and sensitivity can be adjusted via the blue potentiometer.

##### MQ-2 Gas Sensor :
- [MQ2][mq2] Sensor is one of the commonly used gas sensors in MQ sensor series. It is a Metal Oxide Semiconductor (MOS) type Gas Sensor also known as Chemiresistors as the detection is based upon change of resistance of the sensing material when the Gas comes in contact with the material. Using a simple voltage divider network, concentrations of gas can be detected.
- It can detect LPG, Smoke, Alcohol, Propane, Hydrogen, Methane and Carbon Monoxide concentrations anywhere from 200 to 10000ppm.

##### Nodemcu ESP8266-12E :
- [NodeMCU ESP8266-12E][esp] is an open-source Lua based firmware and development board specially targeted for IoT based Applications. It includes firmware that runs on the ESP8266 Wi-Fi SoC from Espressif Systems, and hardware which is based on the ESP-12 module.
- Nodemcu ESP8266-12E [dataset][dataset] can be used to get more detailed information about it.

##### Micropython:
- [MicroPython][micropython] is a lean and efficient implementation of the Python 3 programming language that includes a small subset of the Python standard library and is optimised to run on microcontrollers and in constrained environments.
- More Details are available on the [official website][micropython-official].

### Developers :-

| Name | USN | EMAIL|
| ------ | ------ | ------ |
| Gude Neeraja | 1MJ18CS712 | neeru.gvr@gmail.com |
| Donthamsetty Yasaswini | 1MJ18CS708 | donthamsettyyasashwini@gmail.com |
| Neppalli Sai Krishna | 1MJ18CS719 | nsaikrishna19@outlook.com |

## License
MIT

[micropython-official]: <https://micropython.org/>
[micropython]: <https://en.wikipedia.org/wiki/MicroPython>
[Flame]: <https://www.elprocus.com/flame-sensor-working-and-its-applications/>
[mq2]: <https://lastminuteengineers.com/mq2-gas-senser-arduino-tutorial/>
[dataset]: <https://components101.com/development-boards/nodemcu-esp8266-pinout-features-and-datasheet>
[esp]: <https://en.wikipedia.org/wiki/NodeMCU>
