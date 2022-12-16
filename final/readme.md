This is the codebase for my final project: The Magical "Where-Ya-At" Clock.

The only file active here is "Clock_01.py". Simply running this connect to the CloudMQTT broker, and subscribe to incoming
messages from the OwnTracks app. The file uses the paho.mqtt, json, datetme, time, and RPi.GPIO libraries. The motor pins are
defined in the file, and to create proper rotation, the pins must be wired in as described.

