#!/bin/bash

rm -rf out result
mkdir out result
./nyanbc.py
convert -loop 0 out/*.png -resize 540x540 result/nyanbc.gif
