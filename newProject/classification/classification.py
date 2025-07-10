import fitz  
import os
import re

from strings import indicator_patterns

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def find_patterns_in_text(text, patterns):
    found = {}
    for pattern in patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            found[pattern] = matches
    return found

# Função principal para processar os PDFs de uma pasta
def process_pdfs_in_folder(folder_path):
    results = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(full_path)
            found = find_patterns_in_text(text, indicator_patterns)
            if found:
                results[filename] = found
    return results

