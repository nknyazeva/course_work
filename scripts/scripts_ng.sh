#!/bin/bash
#PBS -l walltime=100:00:00
#PBS -d.
python negative_control_more_pairs.py 0.1
python negative_control_more_pairs.py 0.2
python negative_control_more_pairs.py 0.3
python negative_control_more_pairs.py 0.4
python negative_control_more_pairs.py 0.5