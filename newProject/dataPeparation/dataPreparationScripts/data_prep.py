import argparse
from dataPreparationTools.data_conversion import wos_to_excel, excel_to_wos
from dataPreparationTools.get_missing_data import fill_missing_fields
from dataPreparationTools.file_manager import get_next_output_filename

FUNCTIONS = {
    "wos_to_excel": wos_to_excel,
    "excel_to_wos": excel_to_wos,
    "fill_missing_data": fill_missing_fields
}



def main():
    parser = argparse.ArgumentParser(description="Run one of the available operations.")
    parser.add_argument("function", choices=FUNCTIONS.keys(), help="Function to execute")
    parser.add_argument("input_file", help="Path to the input file")

    args = parser.parse_args()
    func = FUNCTIONS[args.function]

    if(args.function == "excel_to_wos"):
        output_file = get_next_output_filename(".txt")
    else:
        output_file = get_next_output_filename(".xlsx")
    
    try:
        print(f"Running {args.function} with file {args.input_file}...")
        result = func(args.input_file, output_file)
        print("Success:", result)
    except Exception as e:
        print(f"Failure: {e}")

if __name__ == "__main__":
    main()
