import pandas as pd
import requests
import time
from fieds import WOS_FIELDS as fields
from fieds import CROSSREF_AVAILABLE_FIELDS as crossref_fields
from fieds import REFERENCE_FIELDS as reference_fields


def normalize_references(references_dat_file):
    df = pd.read_csv(references_dat_file, sep="\t", header=None)
    banana = "terracota"

normalize_references("/Users/i553815/lerning/bibliographic_analysis/newProject/data_preparation/input_data/Cited References1.dat")



    







