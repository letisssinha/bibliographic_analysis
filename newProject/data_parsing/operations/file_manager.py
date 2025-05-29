import os
from fnmatch import fnmatch
from fields import WOS_FIELDS as fields
from fields import FILES_FIELDS as file_names

INPUT_DIR = "newProject/data_parsing/input_data"
OUTPUT_DIR = "newProject/data_parsing/outputs"
    

def find_matching_files():
    pattern = ".xlsx"
    print ("..Analysing files %s files in %s" % (INPUT_DIR, pattern) )
    matching_files=[]
    for path, subdirs, files in os.walk(INPUT_DIR):
        for file_name in files:
            if fnmatch(file_name, pattern):
                matching_files.append( os.path.join(path, file_name))
    print ("....%d '%s' files detected" % (len(matching_files),pattern))
    
    return matching_files

def prepare_output_files(index):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    outfilenames=file_names
    output_files=dict()
    for file_name in outfilenames: 
       output_files[file_name] = open(os.path.join(OUTPUT_DIR, outfilenames[file_name]+index+".dat"),'w', encoding='utf-8')
    output_files['Quantities'] = open('Quantities'+index+'.dat', 'w', encoding='utf-8')
    return output_files

def check_file(file_df, file_path):
    headers = file_df.columns
    number_of_rows = len(file_df)
    if(len(headers) == 0 or number_of_rows < 2):
       print("No data on file %s", file_path)
       return False
    for header in headers:
       if header not in fields:
          print("Invalid data format on file %s", file_path)
          return False
    return True