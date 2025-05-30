# -*- coding: utf-8 -*-

from file_manager import *
import pandas as pd


def data_parser():
   input_files = find_matching_files()
   for file in input_files:
      df = pd.read_excel(file)
      if not check_file(df, file):
         continue
      print ("..processing citations in file %s" %  file)
      output_files = prepare_output_files()
      file_parser(df, output_files)


def file_parser(df, output_files):
  number_of_citations = df.shape[0]
  if(number_of_citations > 0):
      quantities = make_quantities_array(file_names.values())
      for index, citation in df.iterrows():
         citation_output(str(index), output_files, citation)
         for key, value in file_names.items():
            if not pd.isna(citation[value]):
               value_row = str(index) + ' ' + str(quantities[value]) + ' '
               value_row = value_row + str(citation[value])
               value_row = value_row.replace("\n", " ")
               output_files[value].write(value_row + "\n")
               quantities[value] = quantities[value] + 1
      write_quantities_file(quantities, output_files)

  for file in file_names.values(): output_files[file].close()

def citation_output(index, output_files, citation):
   citation_row = index + ' '
   citation_row = citation_row + ' '.join(map(str, citation.values))
   citation_row = citation_row.replace("\n", " ")
   output_files['Citations'].write(citation_row)
   output_files['Citations'].write("\n")


def make_quantities_array(names):
   quantities = dict()
   for name in names:
      quantities[name] = 0
   return quantities

def write_quantities_file(quantities, output_files):
   quantities_file = output_files['Quantities']
   for name, quantity in quantities.items():
      quantities_file.write(name + ": " + str(quantity) + "\n")

