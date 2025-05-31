import pandas as pd
from fields import FREQUENCY_FIELDS as file_names_dict

INPUT_DIR = "newProject/corpus_description/input_data/"
DAT_FORMAT = ".dat"
FILES_NAMES = file_names_dict.values()
COLUMN_NAMES = ["citation_index", "item_index", "citation_item"]
ITEMS_COLUMN = COLUMN_NAMES[2]
INDEX_COLUMN = COLUMN_NAMES[0]

def calculate_unique_id_items(input_file_name, index):
   column_names = ["citation_index", "item_index", "citation_item"]
   input_file_path = INPUT_DIR + input_file_name + str(index) + DAT_FORMAT 
   df = pd.read_csv(input_file_path, sep="\t", header=None, names=column_names)
   return df["citation_item"].nunique()








