# -*- coding: utf-8 -*-

from file_manager import *
import pandas as pd

from wordfreq import top_n_list
COMMON_WORDS =  top_n_list('en', 1000)

import spacy



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
               if key == "DE" or key == "CR" or key == "AU" or key == "TI" or key == "AB":
                  quantities[value] = parse_multi_content_file(citation[value], str(index), quantities[value], output_files[value], key)
               elif key == "C1" or key == "TC" or key == "PY":
                  quantities[value] = parse_normal_files(str(index), quantities[value], citation[value], output_files[value])
      write_quantities_file(quantities, output_files)

  for file in file_names.values(): output_files[file].close()

def citation_output(index, output_files, citation):
   citation_row = index + '\t'
   citation_row = citation_row + '\t'.join(map(str, citation.values))
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

def parse_multi_content_file(value_line, citation_index, value_quantities, value_file, key):
   if key == "TI" or key == "AB":
      nlp = spacy.load("en_core_web_sm")
      value_line_spacy = nlp(value_line)
      values = [token.text.lower() for token in value_line_spacy if token.is_alpha]
   else:
      values = value_line.split("; ")
   for value in values:
      if value == "" or value == " " or value in COMMON_WORDS:
         continue
      value = value.replace("\n", "")
      line = str(citation_index) + "\t" + str(value_quantities) + "\t" + value
      value_file.write(line + "\n")
      value_quantities = int(value_quantities) + 1
   return value_quantities

def parse_normal_files(index, quantities, value, output_file):
   value_row = str(index) + '\t' + str(quantities) + '\t'
   value_row = value_row + str(value)
   value_row = value_row.replace("\n", " ")
   output_file.write(value_row + "\n")
   return quantities + 1




