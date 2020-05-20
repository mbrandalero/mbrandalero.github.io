#!/usr/bin/python

import urllib.request

from abc import abstractmethod

import xml.etree.ElementTree as ET

myname = "M. Brandalero"

class Author:

    def __init__(self, name, pid=None, orcid=None):
        self.name = name
        self.pid = pid
        self.orcid = orcid

    def to_txt(self, form):
        out = ""
        if form == "N.M.LastName":
            names = self.name.split()

            for i in range(0, len(names)-1):
                out += names[i][0] + ". "
            out += names[len(names)-1]
            
        else:
            out = self.name

        return out

class Paper:

    def __init__(self, title, authors, year):
        self.title = title
        self.authors = authors
        self.year = year

    def to_cventry(self):
        out = "\cventry{" + f"{self.year}" + "}{"
        for author in self.authors:
            name = author.to_txt("N.M.LastName")
            if name != myname:
                name = "{\\normalfont " + name + "}"
            out += name + ", "
        out = out[:-2] + "}{"

        out += f"{self.title}" + "}"

        return outs
    
    def to_item(self):
        out = "\item "# + f"({self.year}) "
        for author in self.authors:
            name = author.to_txt("N.M.LastName")
            if name == myname:
                name = "\\textbf{" + name + "}"
            out += name + ", "
        out = out[:-2] + ". "

        out += "\emph{" + f"{self.title}" + "}. "

        return out

    def to_html(self):
        out = "[" + f"{self.year}" + "] "
        for author in self.authors:
            name = author.to_txt("N.M.LastName")
            if name == myname:
                name = "<b> " + name + "</b>"
            out += name + ", "
        out = out[:-2] + ". "

        out += "<i>" + f"{self.title}" + "</i> "

        return out
    
class JournalPaper(Paper):

    def set(self, journal=None, volume=None, pages=None, doi=None):
        self.journal = journal
        self.volume = volume
        self.pages = pages
        self.doi   = doi

    def to_cventry(self):
        out = super().to_cventry()

        out += "{" + f"In: {self.journal}, v. {self.volume}, "
        if self.pages is not None:
            out += f"{self.pages}, " 
        out += f"{self.year}." + "}{"
        
        for doi in self.doi:
            out += "\\href{" + f"{doi}" + \
                "}{ {\\color{blue}\\ttfamily [doi]}}"
        out += "}{}"
            
        return out

    def to_item(self):
        out = super().to_item()

        out += \
            f"In: {self.journal}, v. {self.volume}, p. {self.pages}, " + \
            f"{self.year}. "
        
        for doi in self.doi:
            out += "\\href{" + f"{doi}" + \
                "}{ {\\color{blue}\\ttfamily [doi]}}"
            
        return out

    def to_html(self):
        out = super().to_html()

        out += \
            f"In: {self.journal}, v. {self.volume}, p. {self.pages}, " + \
            f"{self.year}. "
        
        for doi in self.doi:
            out += "<a href=\"" + f"{doi}" + \
                "\"> [doi] </a>"
            
        return out
    
class ConfPaper(Paper):
    def set(self, booktitle=None, pages=None, doi=None):
        self.booktitle = booktitle
        self.pages = pages
        self.doi   = doi

    def to_cventry(self):
        out = super().to_cventry()

        out += "{" + f"In: {self.booktitle} {self.year}, pp. {self.pages}" + \
            "}{"
        
        for doi in self.doi:
            out += "\\href{" + f"{doi}" + \
                "}{ {\\color{blue}\\ttfamily [doi]}}"
        out += "}{}"
        
        return out

    def to_item(self):
        out = super().to_item()

        out += f"In: {self.booktitle} {self.year}, pp. {self.pages}. "
        
        for doi in self.doi:
            out += "\\href{" + f"{doi}" + \
                "}{ {\\color{blue}\\ttfamily [doi]}}"
        
        return out

    def to_html(self):
        out = super().to_html()

        out += f"In: {self.booktitle} {self.year}, pp. {self.pages}. "
        
        for doi in self.doi:
            out += "<a href=\"" + f"{doi}" + \
                "\">[doi]</a>"
        
        return out
    
def main():
    
    url = "http://dblp.uni-trier.de/pers/xx/b/Brandalero:Marcelo.xml"
    response = urllib.request.urlopen(url)
    data = response.read()
    xmlin = data.decode('utf-8')
    with open("publications.xml", "w") as f:
        f.write(xmlin)
        
    root = ET.fromstring(xmlin)


    journal_publ = []
    for publ in root.findall("*/article"):

        authors = []
        for a in publ.findall("author"):
            name = a.text
            authors.append(Author(name))

        title   = publ.find("title").text
        journal = publ.find("journal").text
        try:
            pages   = publ.find("pages").text
        except:
            pages   = None
        volume  = publ.find("volume").text
        year    = publ.find("year").text

        doi       = []
        for d in publ.findall("ee"):
            doi += [d.text]

        j = JournalPaper(title, authors, year)
        j.set(journal, volume, pages, doi)
        journal_publ.append(j)

    conf_publ = []
    for publ in root.findall("*/inproceedings"):

        authors = []
        for a in publ.findall("author"):
            name = a.text
            authors.append(Author(name))

        title     = publ.find("title").text
        booktitle = publ.find("booktitle").text
        pages     = publ.find("pages").text
        year      = publ.find("year").text

        doi       = []
        for d in publ.findall("ee"):
            doi += [d.text]

        c = ConfPaper(title, authors, year)
        c.set(booktitle, pages, doi)
        conf_publ.append(c)

    publications = sorted(journal_publ + conf_publ,
                          key = lambda publ : publ.year, reverse = True)

    print("<h1 id=\"conference-publications\">Conference Publications</h1>\n")    
    for publ in sorted(conf_publ, key = lambda publ : publ.year, reverse = True):
        print("<p>" + publ.to_html() + "<\p>\n")
        
    print("<h1 id=\"journal-publications\">Journal Publications</h1>\n")    
    for publ in sorted(journal_publ, key = lambda publ : publ.year, reverse = True):
        print("<p>" + publ.to_html() + "<\p>\n")
        
if __name__ == "__main__":
    main()
