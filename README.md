TekRice
===================

Star topology sensor network designed using Freaklabs open hardware. Hatake (畑) is the Japanese name for "rice field". This repository contains the code for a system designed to monitor the water level in rice fields and upload the data to a server.

This is an open source / open hardware collaboration by [Freaklabs](http://www.freaklabs.org/), Hacker Farm and [Future Lab](http://www.fljapan.com/).

## Folder structure and architecture

*  FLChibiLib

C library with common constants and functions used by sensor nodes (Data collection) and the aggregator node

* collection

Arduino Code that runs on sensor nodes. It reads data from sensor attached to the Chibi-900 v2.1 and sends it to the aggregation node using chibiTx.

* aggregation

Code that runs on the aggregation node.

scan_serial.py reads from the serial port and sends data to a server. This code should run on a computer attached to the Chibi-900 v2.1 that is acting as aggregator.

* REST_api

API that can be used to read the latest readings made by the sensor nodes. This API code runs on the same server where the aggregation node sends the data.

## How to setup the system

Step 1: upload collection/collect_temperature/collect_temperature.ino to each temperature collection node.

Step 2: upload aggregation/aggregator.ino on the aggregation node.

Step 3: run aggregation/scan_serial.py on the computer attached to the aggregation node.

Step 4: execute REST_api/run.py

Step 5: open localhost on your browser

This is how our setup looks with two temperature sensor nodes:

![alt tag](http://www.fljapan.com/wp-content/uploads/2014/08/hatake1.jpg)

## Hardware

For the data collection nodes we are using [Freakduinos v2.1a] (http://www.freaklabs.org/index.php/Tutorials/Hardware/Assembling-the-Freakduino-v2.1a.html) . We use the [chibi Arduino](https://github.com/freaklabs/chibiArduino) lightweight 802.15.4 protocol stack.

The sensors used to measure the water level are [Parallax PING))) Ultrasonic Distance Sensor (#28015)](http://www.parallax.com/sites/default/files/downloads/28015-PING-Sensor-Product-Guide-v2.0.pdf)


# Things to do for initial test-deployment in November

##Trial run - Have the system run for a week without fail
Let’s deploy a saboten on the DG roof. If range is a problem we can leave the edge node of Dave’s desk, or Hector can sneak it into Hayashisans office next time he has a meeting there.


###Backend
Use Satoyama API. It’s more or less ready for what we need. 


###Edge node improments
- Still some stability issues that are buggering the hell out of me
- Fuck the admins and let’s get a 3G shield. We’ll need it for deployment anyway.

### Sensor nodes
- Figure out how use the PCF2127AT to do local timestamping
- Decrease transmission interval
- Power management - sleep between transmitting

### Release the system into the wild
- Test battery lifetime of saboten with solar panel
- Decide location for edge node
-- Requires access to power grid

### Long term plan


##PCB improvements
- GPS chip for automatically transmitting node position on power-up, or on request from api
- GPS should of course be turned off most of the time.


## Sonar 
- keyword is low-cost, so the one Chris showed us on hacker farm is probably too expensive (he said it was around 200USD, right?)
- We don’t need long range, but diffusion should be less than the ones we’re using now (right?)




