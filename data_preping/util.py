
def read_text_file_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as text_file:
        return text_file.readlines()
    
