#!/bin/bash

rm -rf out
mkdir out
./nyanbc.py
convert -loop 0 out/*.png -resize 640x640 result/nyanbc.gif
