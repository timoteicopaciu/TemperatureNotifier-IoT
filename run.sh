#!/bin/sh
sudo pigpiod
> output.txt
nohup python3 -u temperatureNotifier.py > output.txt &
