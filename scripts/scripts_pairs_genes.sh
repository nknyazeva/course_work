#!/bin/bash
#PBS -l walltime=100:00:00
#PBS -d.
python counting_frequency_pairs_genes_by_threshold.py 0.1
python counting_frequency_pairs_genes_by_threshold.py 0.2
python counting_frequency_pairs_genes_by_threshold.py 0.3
python counting_frequency_pairs_genes_by_threshold.py 0.4
python counting_frequency_pairs_genes_by_threshold.py 0.5