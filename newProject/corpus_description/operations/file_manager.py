import os
from fields import FILES_FIELDS as file_names

INPUT_DIR = "newProject/describe_corpus/input_data"
OUTPUT_DIR = "newProject/describe_corpus/outputs"
OUTPUT_FREQ_DIR = "newProject/describe_corpus/outputs/freq"
FILE_PREFIX = "freq_"
    



##repeated
def get_next_output_filename():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(OUTPUT_FREQ_DIR):
        os.makedirs(OUTPUT_FREQ_DIR)

    existing = [file for file in os.listdir(OUTPUT_FREQ_DIR) if file.endswith(".dat")]
    existing_nums = []

    for file in existing:
        try:
            num = int(file[-5:-4])
            existing_nums.append(num)
        except ValueError:
            continue

    return max(existing_nums, default=0) + 1
