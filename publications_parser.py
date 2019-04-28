#!/bin/python3

import bibtexparser
from bibtexparser.bparser import BibTexParser

import sys

yaml_header = \
    "---\n" + \
    "layout: page\n" + \
    "title: Publications\n" + \
    "subtitle: Marcelo Brandalero\n" + \
    "---\n\n"

def customize_parser(record):

    # 0) Convert to Unicode
    record = bibtexparser.customization.convert_to_unicode(record)
    
    # 1) Fix names
    # 1.1) Convert author names field from str into a list of names
    record = bibtexparser.customization.author(record)
    #print("1.1) " + str(record["author"]))
    
    # 1.2) Take each name in the list and format, adding to a new name string
    formatted_names = ""
    for author in record["author"]:
        formatted_name = ""
        author_names = bibtexparser.customization.splitname(author)

        for first_name in author_names["first"]:
            formatted_name += first_name[0]
        if author_names["von"]:
            formatted_name += " " + author_names["von"][0]
        formatted_name += " " + author_names["last"][0]
        # 1.3) Make my name bold
        if formatted_name == "M Brandalero":
            formatted_name = "**" + formatted_name + "**"

        formatted_names += formatted_name + ", "
        
    record["author"] = formatted_names[:-2]

    #print("1.3) " + str(record["author"]))
          
    return record

parser = BibTexParser(customization = customize_parser)

def main():
  
    with open('publications.bib') as bibtex_file:
        bibtex_db = bibtexparser.load(bibtex_file, parser)
    bibtex_db.entries.sort(key = lambda x : -int(x["year"]))
    
    print(yaml_header)
        
    # Conference Publications
    print("# Conference Publications\n")
    for entry in bibtex_db.entries:
        if entry["ENTRYTYPE"] == "inproceedings":

            print(entry["author"], end = ": ")

            print("*" + entry["title"] + "*", end = ". ")
           
            print("In: " + entry["booktitle"], end = ", ")

            print(entry["year"], end = ".\n\n")

    print("")
    # Journal Publications
    print("# Journal Publications\n")
        
    for entry in bibtex_db.entries:
        if entry["ENTRYTYPE"] == "article":

            print(entry["author"], end = ": ")

            print("*" + entry["title"] + "*", end = ". ")
           
            print(entry["journal"], end = ", ")

            print(entry["year"], end = ".\n\n")
            
if __name__ == "__main__":
    sys_stdout = sys.stdout
    sys.stdout = open("about/publications.md", "w")
    main()
    sys.stdout = sys_stdout
