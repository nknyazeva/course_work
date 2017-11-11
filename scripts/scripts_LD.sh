#!/bin/bash
#PBS -l walltime=100:00:00
#PBS -d.
python LD.py 0.1
python LD.py 0.2
python LD.py 0.3
python LD.py 0.4