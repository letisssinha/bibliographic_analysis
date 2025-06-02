import os
import pandas as pd
import json

from fields import *
from generate_frequency import * 
from generate_coocurrence_network import *




INPUT_DIR = "newProject/corpus_description/input_data/"
DAT_FORMAT = ".dat"
OUTPUT_DIR = "newProject/corpus_description/outputs/freq"
FILE_PREFIX = "freq_"

def calculate_number_of_citations(index):
   input_file_path = INPUT_DIR + 'Citations' + str(index) + DAT_FORMAT 
   df = pd.read_csv(input_file_path, sep="\t", header=None, names=COLUMN_NAMES)
   return len(df)

def make_file_df_without_duplicates(input_file_name, index):
   input_file_path = INPUT_DIR + input_file_name + str(index) + DAT_FORMAT 
   df = pd.read_csv(input_file_path, sep="\t", header=None, names=COLUMN_NAMES)
   item_counts = df[ITEMS_COLUMN].value_counts()
   ##items = sorted(group[ITEMS_COLUMN])
   return df[df[ITEMS_COLUMN].isin(item_counts[item_counts > 1].index)], item_counts

def make_frequency_files(input_file_name, index, df_without_duplicates):
   number_of_citations =  calculate_number_of_citations(index)
   ##too tired to know if df_without_duplicates[ITEMS_COLUMN].value_counts() should be the total number or only the count of unique ones (in the first case, this is wrong and the item count should be obtained from the previous function)
   frequency_df, item_counts_df = generate_frequency_df(df_without_duplicates, df_without_duplicates[ITEMS_COLUMN].value_counts(), number_of_citations)
   output_path = os.path.join(OUTPUT_DIR, FILE_PREFIX + input_file_name + str(index) + DAT_FORMAT)
   frequency_df.to_csv(output_path, index=False, columns=[ITEMS_COLUMN, COUNT_COLUMN, FREQUENCY_COLUMN], float_format='%.2f')

def make_ditribution_file(input_map, total_citations, index):
   all_distributions = {
    "N": total_citations
   }
   for label, df in input_map.items():
      result = calculate_distributions(df)
      breakpoint()
      all_distributions.update(result)
   with open(OUTPUT_DIR + "DISTRIBS_itemuse" + str(index) + DAT_FORMAT, "w", encoding="utf-8") as f:
    json.dump(all_distributions, f, indent=2)

def make_coocurrence_file(index, input_map):
   full_network = {}
   for label, (df, item_counts) in input_map.items():
      net = generate_cooccurrence_network(df, item_counts, label)
      full_network[label] = net

   with open(OUTPUT_DIR + "coocnetworks" + str(index) + DAT_FORMAT, "w") as f:
      json.dump(full_network, f, indent=2)

def describe_corpus(index):
   number_of_citations = calculate_number_of_citations(index)
   for key, file_name in FREQUENCY_FIELDS.items():
      df_without_duplicates, item_counts = make_file_df_without_duplicates(file_name, index)
      make_frequency_files(file_name, index, df_without_duplicates)
   
   frequency_df, item_counts_df = generate_frequency_df(df_without_duplicates, item_counts, number_of_citations)
   coocurrence_input_map = make_coocurrence_input(df_without_duplicates, item_counts, index)
   ditribution_input_map = make_distribution_input(item_counts_df)

   make_coocurrence_file(index, coocurrence_input_map)
   make_ditribution_file(ditribution_input_map, number_of_citations, index)
      

def make_coocurrence_input(df_without_duplicates, item_counts, index):
   input = {}
   for key, file_name in FREQUENCY_FIELDS.items():
      df_without_duplicates, item_counts = make_file_df_without_duplicates(file_name, index)
      input[file_name] = [df_without_duplicates, item_counts]
   return input

def make_distribution_input(item_counts_df):
   input = {}
   for key, file_name in FREQUENCY_FIELDS.items():
      input[file_name] = item_counts_df
   return input













