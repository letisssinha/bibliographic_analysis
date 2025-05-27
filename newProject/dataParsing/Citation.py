import os
import sys
import glob
import numpy
import argparse
import unidecode

class Citation:

    def __init__(self):
        self.citations      = []      # articles list
 
    def read_file(self, filename):

        articles_list = []
        try:
            if filename != 'stdin':
                data_file = open(filename,'rU',encoding='utf-8') 
            else:
                data_file = sys.stdin
            for line in data_file.readlines():
                if line == "EN":
                    break
                line = line.strip('\ufeff') 
                line = line.strip('\n') # removes \n
                wline.parse_line(line, database)
                if line.startswith("ER"):
                    articles_list.append( wline )
                    wline = Biblio_line()
        
        def fill_missing_fields (excel_path, output_path):
            df = pd.read_excel(excel_path)
            for index, citation in df.iterrows():
                fill_missing_field(citation, df, index)
            df.to_excel(output_path, index=False)

            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")
        self.articles   = articles_list