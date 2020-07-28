#!/usr/bin/env python3
##########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2020-07-27
# Purpose: Build database of T-cell receptors labelled by peptide sequence
##########################################################################################

##########################################################################################
# Libraries
##########################################################################################

import csv
import random
import json

##########################################################################################
# Settings
##########################################################################################

path_csv = '../../../Public Data/T-cell_Human_ImmuneCODE-MIRA_Adaptive-Biotech/Samples/20200625/peptide-detail.csv'
path_db = 'db_sequence.json'

generative_split = [ 0.6, 0.2, 0.2 ]

##########################################################################################
# Load
##########################################################################################

samples = {}
with open(path_csv, 'r') as stream:
  reader = csv.DictReader(stream, delimiter=',')
  for row in reader:
    cdr3, vgene, jgene = row['TCR BioIdentity'].split('+')
    experiment = row['Experiment']
    peptide = row['Amino Acids']
    peptide_list = peptide.split(',')
    peptide_list.sort()
    peptide = ','.join(peptide_list)
    if peptide not in samples:
      samples[peptide] = {}
    if cdr3 not in peptide:
      samples[peptide][cdr3] = []
    samples[peptide][cdr3].append(
      {
        'vgene': vgene,
        'jgene': jgene,
        'experiment': experiment  
      }
    )

##########################################################################################
# Seperate samples containing multiple peptides from those containing only one peptide
##########################################################################################

peptides_unique = set()
peptides_degen = set()

for peptide in samples.keys():
  if ',' in peptide:
    peptides_degen.add(peptide)
  else:
    peptides_unique.add(peptide)

peptides_unique = list(peptides_unique)
peptides_degen = list(peptides_degen)

##########################################################################################
# Split samples into a training, validation, and test cohort
##########################################################################################

db_gen = {
  'train': {},
  'validate': {},
  'test': {},
  'all': {}
}

for peptides in [ peptides_unique, peptides_degen ]:
  random.shuffle(peptides)
  cumulative_split = 0.0
  splits = [ 0 ]
  for split in generative_split:
    cumulative_split += split
    splits.append(
      int(cumulative_split*len(peptides))
    )
  for i in range(splits[0], splits[1]):
    peptide = peptides[i]
    db_gen['train'][peptide] = samples[peptide]
  for i in range(splits[1], splits[2]):
    peptide = peptides[i]
    db_gen['validate'][peptide] = samples[peptide]
  for i in range(splits[2], splits[3]):
    peptide = peptides[i]
    db_gen['test'][peptide] = samples[peptide]
  for i in range(splits[0], splits[3]):
    peptide = peptides[i]
    db_gen['all'][peptide] = samples[peptide]

##########################################################################################
# Save the database
##########################################################################################

with open(path_db, 'w') as stream:
  json.dump(db_gen, stream, sort_keys=True)

