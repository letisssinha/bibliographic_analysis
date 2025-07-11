import pandas as pd

def excel_to_ris(excel_path, ris_path):
    df = pd.read_excel(excel_path, engine='openpyxl')

    with open(ris_path, 'w', encoding='utf-8') as risfile:
        for _, row in df.iterrows():
            doc_type = str(row.get("Document Type", "")).strip()
            if row.get("Document Type") and row.get("Document Type") != "nan":
                doctype = str(row['Document Type']).strip()
                if doctype == 'J':
                    risfile.write(f"TY  - JOUR\n")
                else:
                    risfile.write(f"TY  - CONF\n")
            
            for author in str(row.get("Authors", "")).split(";"):
                if author.strip() and author.strip() != "nan":
                    risfile.write(f"AU  - {author.strip()}\n")

            if row.get("Title"):
                risfile.write(f"TI  - {str(row['Title']).strip()}\n")

            if row.get("Source"):
                risfile.write(f"JO  - {str(row['Source']).strip()}\n")

            if row.get("Language") and row.get("Language") != "nan":
                risfile.write(f"LA  - {str(row['Language']).strip()}\n")

            if row.get("Abstract") and not row.get("Abstract").startswith("nan")  and not pd.isna(row.get("Abstract")):
                risfile.write(f"AB  - {str(row['Abstract']).strip()}\n")

            if row.get("Publication Year"):
                risfile.write(f"PY  - {str(row['Publication Year']).strip()}\n")

            if row.get("DOI"):
                risfile.write(f"DO  - {str(row['DOI']).strip()}\n")

            if row.get("Times Cited") and row.get("Times Cited") != "nan" and not pd.isna(row.get("Times Cited")):
                risfile.write(f"TC  - {str(row['Times Cited']).strip()}\n")

            for keyword in str(row.get("Keywords", "")).split(";"):
                if keyword.strip() and keyword.strip() != "nan" and not pd.isna(keyword):
                    risfile.write(f"KW  - {keyword.strip()}\n")

            for reference in str(row.get("Cited References", "")).split(";"):
                if reference.strip() and reference.strip() != "nan" and not pd.isna(row.get("Cited References", "")):
                    risfile.write(f"CR  - {reference.strip()}\n")

            risfile.write("ER  -\n\n")


excel_to_ris("newProject/data_preparation/input_data/dataWithReferences.xlsx", "newProject/data_preparation/operations/references.ris")