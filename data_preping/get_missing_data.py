import pandas as pd
import requests
import time
from fieds import WOS_FIELDS as fields
from fieds import CROSSREF_AVAILABLE_FIELDS as crossref_fields
from fieds import REFERENCE_FIELDS as reference_fields

# Crossref search by title
def get_field_from_api(crossref_field, search_term):
    url = "https://api.crossref.org/works"
    params = {"query.bibliographic": search_term, "rows": 1}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = data.get("message", {}).get("items", [])
        if items:
            return items[0][crossref_field]
    except requests.RequestException as e:
        print(f"Request failed for title: {search_term}\nError: {e}")
    return None

def fill_missing_fields (excel_path, output_path):
    df = pd.read_excel(excel_path)
    for index, citation in df.iterrows():
        fill_missing_field(citation, df, index)
    df.to_excel(output_path, index=False)
        

def fill_missing_field(citation, df, index):
    search_term = fields["DI"]
    for citation_field, crossref_field in crossref_fields.items():
            if pd.isna(citation[citation_field]) or str(citation[citation_field]).strip() == '':
                if citation_field == fields["DI"]:
                    search_term = fields["TI"]
                field_value = get_field_from_api(crossref_field, search_term)
                if field_value:
                    if citation_field == fields["CR"]:
                        field_value = parse_references(field_value)
                    if citation_field == fields["PY"]:
                        field_value = parse_year(field_value)
                    print(f" → Found %s: {field_value}", citation_field)
                    df.at[index, citation_field] = field_value
                else:
                    print(" → %s not found.", citation_field)
                time.sleep(1) 

def parse_references(references):
    references_line = ""
    for reference in references:
        reference_text = ""
        for reference_field in reference_fields:
            if reference_field in reference:
                reference_text = reference_text + reference_field + ": " + reference[reference_field] + " "
        references_line = references_line + reference_text + " ;"
    return references_line

def parse_year(date):
    return date["date-parts"][0]

fill_missing_fields("api/output.xlsx", "dataWithReferences.xlsx")




