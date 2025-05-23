import pandas as pd
import fieds as fields

def parse_wos_file(file_path):
    with open(file_path, 'text_file', encoding='utf-8') as file:
        lines = file.readlines()

    records = []
    record = {}

    current_field = None

    for line in lines:
        if line == "":
            continue
        if line[:2] in fields:
            current_field = line[:2]
            value = line[3:]
            record[fields[current_field]] = value
        elif line[:2].strip() == "":
            # Continuation of previous field
            if current_field and fields[current_field] in record:
                record[fields[current_field]] += " " + line.strip()
        elif line.startswith("ER"):
            # End of record
            if record:
                records.append(record)
                record = {}
            current_field = None

    return pd.DataFrame(records)

def wos_to_excel(wos_txt_path, output_excel_path):
    df = parse_wos_file(wos_txt_path)
    df.to_excel(output_excel_path, index=False)
    print(f"Saved Excel file to: {output_excel_path}")

# Example usage
wos_txt_file = 'example_wos.txt'       # Replace with your WoS .txt file path
output_excel_file = 'output.xlsx'      # Desired Excel file name
wos_to_excel(wos_txt_file, output_excel_file)