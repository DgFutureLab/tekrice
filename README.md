hatakeSensorNetwork
===================

Hatake (畑) is the Japanese name for "rice field". This repository contains the code for a system designed to monitor the water level in rice fields and upload the data to a server.

This is an open source / open hardware collaboration by (Freaklabs)[http://www.freaklabs.org/], Hacker Farm and (Future Lab)[http://www.fljapan.com/].

## Folder structure and architecture

1.  FLChibiLib

C library with common constants and functions used by sensor nodes (Data collection) and the aggregator node

2. collection

Arduino Code that runs on sensor nodes. It reads data from sensor attached to the Chibi-900 v2.1 and sends it to the aggregation node using chibiTx.

3. aggregation

Code that runs on the aggregation node.

scan_serial.py reads from the serial port and sends data to a server. This code should run on a computer attached to the Chibi-900 v2.1 that is acting as aggregator.

4. REST_api

API that can be used to read the latest readings made by the sensor nodes. This API code runs on the same server where the aggregation node sends the data.

## Hardware

For the data collection nodes we are using [Freakduinos v2.1a] (http://www.freaklabs.org/index.php/Tutorials/Hardware/Assembling-the-Freakduino-v2.1a.html) . We use the [chibi Arduino](https://github.com/freaklabs/chibiArduino) lightweight 802.15.4 protocol stack.

The sensors used to measure the water level are [Parallax PING))) Ultrasonic Distance Sensor (#28015)](http://www.parallax.com/sites/default/files/downloads/28015-PING-Sensor-Product-Guide-v2.0.pdf)