#!/bin/sh

python kg/run_transe.py --fin data/wn18.bin \
       --test-all 50 --nb 100 --me 1000 \
       --margin 2 --lr 0.01 --ncomp 20
