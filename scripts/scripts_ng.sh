#!/bin/bash
#PBS -l walltime=100:00:00
#PBS -d.
python negative_control.py 0.1
python negative_control.py 0.2
python negative_control.py 0.3
python negative_control.py 0.4