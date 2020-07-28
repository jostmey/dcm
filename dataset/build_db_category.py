#!/usr/bin/env python3
##########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2020-02-29
# Purpose: Build database of T-cell receptors labelled by peptide category
##########################################################################################

##########################################################################################
# Libraries
##########################################################################################

import json
import random

##########################################################################################
# Settings
##########################################################################################

path_db_gen = 'db_sequence.json'
path_db_class = 'db_category.json'

classification_split = [ 0.6, 0.2, 0.2 ]
min_count = 100

random.seed(7424103)

##########################################################################################
# Load
##########################################################################################

with open(path_db_gen, 'r') as stream:
  db_gen = json.load(stream)

##########################################################################################
# Split samples into a training, validation, and test cohort
##########################################################################################

db_class = {
  'train': {},
  'validate': {},
  'test': {},
  'all': {}
}

for split_gen in [ 'train', 'validate' ]:
  samples = db_gen[split_gen]
  for peptide in sorted(samples.keys()):
    cdr3s = samples[peptide]
    if len(cdr3s) >= min_count:
      cdr3s_list = sorted(list(cdr3s.keys()))
      random.shuffle(cdr3s_list)
      cumulative_split = 0.0
      splits = [ 0 ]
      for split in classification_split:
        cumulative_split += split
        splits.append(
          int(cumulative_split*len(cdr3s))
        )
      db_class['train'][peptide] = {}
      for i in range(splits[0], splits[1]):
        cdr3 = cdr3s_list[i]
        entries = cdr3s[cdr3]
        db_class['train'][peptide][cdr3] = entries
      db_class['validate'][peptide] = {}
      for i in range(splits[1], splits[2]):
        cdr3 = cdr3s_list[i]
        entries = cdr3s[cdr3]
        db_class['validate'][peptide][cdr3] = entries
      db_class['test'][peptide] = {}
      for i in range(splits[2], splits[3]):
        cdr3 = cdr3s_list[i]
        entries = cdr3s[cdr3]
        db_class['test'][peptide][cdr3] = entries
      db_class['all'][peptide] = {}
      for i in range(splits[0], splits[3]):
        cdr3 = cdr3s_list[i]
        entries = cdr3s[cdr3]
        db_class['all'][peptide][cdr3] = entries

##########################################################################################
# Save the database
##########################################################################################

with open(path_db_class, 'w') as stream:
  json.dump(db_class, stream, sort_keys=True)

