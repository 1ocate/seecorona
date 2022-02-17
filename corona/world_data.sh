#!/bin/bash

curl -s https://www.worldometers.info/coronavirus/ > /root/corona/world.temp.html
mv -f /root/corona/world.temp.html /root/corona/world.html
#python3 world_list.py
