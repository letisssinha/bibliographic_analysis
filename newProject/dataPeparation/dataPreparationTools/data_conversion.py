import pandas as pd
from newProject.utils.fieds import WOS_FIELDS as fields


def read_text_file_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as text_file:
        return text_file.readlines()

def store_wos_file_content_into_data_frame(file_path):
    lines = read_text_file_lines(file_path)
    citations = []
    citation = {}
    for line in lines:
        if line == "":
            continue
        elif line.startswith("EN"):
            break
        elif line.startswith("ER"):
             append_citation_to_list(citation, citations)
             citation = {}
        make_record_field(line, citation)
    return pd.DataFrame(citations)

def make_record_field(line, citation):
    line_field_tag = line[:2]
    if line_field_tag in fields:
            line_value = line[3:]
            citation[fields[line_field_tag]] = line_value

def append_citation_to_list(citation, citations):
     if citation:
        citations.append(citation)

def write_citation_into_wos(citation, out):
     for tag, field in fields.items():
        value = citation.get(field, "")
        if pd.isna(value):
            continue
        out.write(f"{tag}  {value}")
        
def wos_to_excel(wos_file_path, output_excel_path):
    df = store_wos_file_content_into_data_frame(wos_file_path)
    df.to_excel(output_excel_path, index=False)

def excel_to_wos(excel_path, txt_output_path):
    df = pd.read_excel(excel_path)
    with open(txt_output_path, 'w', encoding='utf-8') as out:
        for _, citation in df.iterrows():
            write_citation_into_wos(citation, out)
            out.write(f"ER\n\n")
        out.write(f"EN")  # End of record

