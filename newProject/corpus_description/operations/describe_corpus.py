import os
import pandas as pd
from collections import Counter
from itertools import combinations
import json

from file_manager import prepare_output_files
from fields import *
from generate_frequency import * 
from generate_coocurrence_network import *




INPUT_DIR = "newProject/corpus_description/input_data/"
DAT_FORMAT = ".dat"
OUTPUT_DIR = "newProject/corpus_description/input_data/"
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
   return df[df[ITEMS_COLUMN].isin(item_counts[item_counts > 1].index)]

def make_frequency_files(input_file_name, index):
   number_of_citations =  calculate_number_of_citations(index)
   df_without_duplicates = make_file_df_without_duplicates(input_file_name, index)
   ##too tired to know if df_without_duplicates[ITEMS_COLUMN].value_counts() should be the total number or only the count of unique ones (in the first case, this is wrong and the item count should be obtained from the previous function)
   frequency_df = generate_frequency_df(df_without_duplicates, df_without_duplicates[ITEMS_COLUMN].value_counts(), number_of_citations)
   output_path = os.path.join(OUTPUT_DIR, FILE_PREFIX + input_file_name + index + DAT_FORMAT)
   frequency_df.to_csv(output_path, index=False, columns=[ITEMS_COLUMN, COUNT_COLUMN, FREQUENCY_COLUMN], float_format='%.2f')

def make_ditribution_file(label_to_df_map, total_citations, index):
   all_distributions = {
    "N": total_citations
   }
   for label, df in label_to_df_map.items():
      result = calculate_distributions(df, f"p{label}")
      all_distributions.update(result)
   with open(OUTPUT_DIR + "DISTRIBS_itemuse" + index + DAT_FORMAT, "w", encoding="utf-8") as f:
    json.dump(all_distributions, f, indent=2)

def make_coocurrence_file(index):
   full_network = {}
   for label, (df, item_counts) in label_to_data.items():
      net = generate_cooccurrence_network(df, item_counts, label)
      full_network[label] = net

   with open(OUTPUT_DIR + "coocnetworks" + index + DAT_FORMAT, "w") as f:
      json.dump(full_network, f, indent=2)









