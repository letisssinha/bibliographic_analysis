import os
from fields import FILES_FIELDS as file_names

INPUT_DIR = "newProject/describe_corpus/input_data"
OUTPUT_DIR = "newProject/describe_corpus/outputs"
OUTPUT_FREQ_DIR = "newProject/describe_corpus/outputs/outputs/freq"
FILE_PREFIX = "freq_"
    

##repeated
def prepare_output_files():
    index = str(get_next_output_filename())
    outfilenames=file_names
    output_files=dict()
    for key, file_name in outfilenames.items(): 
        output_files[file_name] = open(os.path.join(OUTPUT_DIR, FILE_PREFIX + outfilenames[key]+index+".dat"),'w', encoding='utf-8')
    output_files['Citations'] = open(os.path.join(OUTPUT_DIR, FILE_PREFIX+ 'Citations'+index+'.dat'), 'w', encoding='utf-8')
    return output_files


##repeated
def get_next_output_filename():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
def get_next_output_filename():
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