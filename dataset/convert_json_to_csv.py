#!/usr/bin/env python3
##########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2020-02-29
# Purpose: Convert json database to CSV files of each dataset
##########################################################################################

##########################################################################################
# Libraries
##########################################################################################

import argparse
import json

##########################################################################################
# Settings
##########################################################################################

parser = argparse.ArgumentParser()
parser.add_argument('--db', help='Path to the json database', type=str, required=True)
parser.add_argument('--output', help='Basename for CSV output files', type=str, required=True)
args = parser.parse_args()

##########################################################################################
# Load database
##########################################################################################

with open(args.db, 'r') as stream:
  db = json.load(stream)

##########################################################################################
# Save datasets
##########################################################################################

for split in [ 'train', 'validate', 'test', 'all' ]:
  with open(args.output+'_'+split+'.csv', 'w') as stream:
    print(
      'CDR3', 'Vgene', 'Jgene', 'Peptide', 'Frequency', 'Experiment',
      sep=',', file=stream
    )
    samples = db[split]
    num_peptides = len(samples)
    for peptide in sorted(samples.keys()):
      cdr3s = samples[peptide]
      num_cdr3s = len(cdr3s)
      for cdr3 in sorted(cdr3s.keys()):
        entries = cdr3s[cdr3]
        peptide_ = ':'.join(peptide.split(','))
        num_entries = len(entries)
        for entry in entries:
          frequency = 1.0/(num_peptides*num_cdr3s*num_entries)
          print(
            cdr3, entry['vgene'], entry['jgene'], peptide_, frequency, entry['experiment'],
            sep=',', file=stream
          )
