Techrice
===================

Techrice is an open data sensor network based in Kamogawa, Japan. Techrice wants to help local farmers monitoring rice fields water levels.

Star topology sensor network designed using Freaklabs open hardware. Hatake (畑) is the Japanese name for "rice field". This repository contains the code for a system designed to monitor the water level in rice fields and upload the data to a server.

This is an open source / open hardware collaboration by [Freaklabs](http://www.freaklabs.org/), Hacker Farm and [Future Lab](http://www.fljapan.com/).

## Hardware

For the data collection nodes we are using [Freakduinos v2.1a] (http://www.freaklabs.org/index.php/Tutorials/Hardware/Assembling-the-Freakduino-v2.1a.html) . We use the [chibi Arduino](https://github.com/freaklabs/chibiArduino) lightweight 802.15.4 protocol stack.

The sensors used to measure the water level are [Parallax PING))) Ultrasonic Distance Sensor (#28015)](http://www.parallax.com/sites/default/files/downloads/28015-PING-Sensor-Product-Guide-v2.0.pdf)