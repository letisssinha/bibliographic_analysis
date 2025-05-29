#! /usr/bin/python -v
# -*- coding: utf-8 -*-

""" 
   Author : Sebastian Grauwin (http://www.sebastian-grauwin.com/)
   Copyright (C) 2017
"""

# usage: parser.py -i DIR [-o DIR] [-e]
# 

from file_manager import *
import pandas as pd


def data_parser():
   input_files = find_matching_files()
   i = 1
   for file in input_files:
      df = pd.read_excel(file)
      if not check_file(df, file):
         continue
      print ("..processing citations in file %s" %  file)
      output_files = prepare_output_files(i)
      file_parser(df, output_files)


def file_parser(df, output_files):
  number_of_citations = df.size()
  if(number_of_citations > 0):
      for index, citation in df.iterrows():
         citation_row = index + ' '
         citation_row = citation_row + ' '.join(map(str, citation.values))
         output_files['Citations'].write(citation_row)
         i = 0
         for key, value in file_names:
            if citation[value]:
               value_row = index + ' ' + i + ' '
               value_row = value_row + citation[value]
               output_files[value].write(value_row)
  for file in file_names: output_files[file].close()
