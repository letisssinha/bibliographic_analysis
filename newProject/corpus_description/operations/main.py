import argparse
from describe_corpus import  describe_corpus
from file_manager import get_next_output_filename

##python3 newProject/corpus_description/operations/main.py 


def main():
    ##todo exceptions
    index = get_next_output_filename()
    describe_corpus(index)
    print(f"Result Files where created")

if __name__ == "__main__":
    main()








