import argparse
from biblio_parser import  data_parser


def main():
    ##todo exceptions
    data_parser()
    print(f"Result Files where created")

if __name__ == "__main__":
    main()
