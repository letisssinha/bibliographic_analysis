#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" 
   Author : Sebastian Grauwin (http://www.sebastian-grauwin.com/)
   Copyright (C) 2012
   All rights reserved.
   BSD license.
"""

import os
import sys
import glob
import numpy
import argparse
import unidecode

def remove_accents(input_str):
    return unidecode.unidecode(input_str)

## ##################################################
## ##################################################
## ##################################################

class Biblio_line:
    def __init__(self):
        self.PT = "" ## Publication Type (J=Journal; B=Book; S=Series)
        self.AU = "" ## Authors
        self.BA = "" ## Book Authors
        self.BE = "" ## Book Editor
        self.GP = "" ## Book Group Authors
        self.AF = "" ## Author Full Name
        self.BF = "" ##         
        self.CA = "" ## Group Authors
        self.TI = "" ## Document Title
        self.SO = "" ## Publication Name
        self.SE = "" ## Book Series Title
        self.BS = "" ## Book Series Subtitle
        self.LA = "" ## Language
        self.DT = "" ## Document Type
        self.CT = "" ## Conference Title 
        self.CY = "" ## Conference Date 
        self.CL = "" ## Conference Location 
        self.SP = "" ## Conference Sponsors 
        self.HO = "" ## Conference Host
        self.DE = "" ## Author Keywords
        self.ID = "" ## Keywords Plus
        self.AB = "" ## Abstract
        self.C1 = "" ## Author Address
        self.RP = "" ## Reprint Address
        self.EM = "" ## E-mail Address
        self.RI = "" ##
        self.OI = "" ##
        self.FU = "" ## Funding Agency and Grant Number
        self.FX = "" ## Funding Text
        self.CR = "" ## Cited References
        self.NR = "" ## Cited Reference Count
        self.TC = "" ## Times Cited
        self.Z9 = "" ## 
        self.PU = "" ## Publisher
        self.PI = "" ## Publisher City
        self.PA = "" ## Publisher Address
        self.SN = "" ## ISSN
        self.EI = "" ##
        self.BN = "" ## ISBN
        self.J9 = "" ## 29-Character Source Abbreviation
        self.JI = "" ## ISO Source Abbreviation
        self.PD = "" ## Publication Date
        self.PY = 0 ## Year Published
        self.VL = "" ## Volume
        self.IS = "" ## Issue
        self.PN = "" ## Part Number
        self.SU = "" ## Supplement
        self.SI = "" ## Special Issue
        self.BP = "" ## Beginning Page
        self.EP = "" ## Ending Page
        self.AR = "" ## Article Number
        self.DI = "" ## Digital Object Identifier (DOI)
        self.D2 = "" ## 
        self.PG = "" ## Page Count
        self.WC = "" ## Web of Science Category
        self.SC = "" ## Subject Category
        self.GA = "" ## Document Delivery Number
        self.UT = "" ## Unique Article Identifier

    def parse_line(self, line, database):
        line_data = line[3:]
        if database =='wos':
            Cols = ['PT', 'AU', 'TI', 'SO', 'SN', 'DT', 'DE', 'ID', 'AB', 'C1', 'RP', 'CR', 'TC', 'J9', 'PD', 'PY', 'LA', 'VL', 'IS', 'BP', 'WC', 'FX', 'DI', 'UT']
            for col in Cols:
                if line.startswith(col):
                    if line.startswith('PY') and line!= "nan":
                        line_data = int(line_data[:4])
                    setattr(self, col, line_data)


class ArticleList:

    def __init__(self):
        self.articles      = []      # articles list
 
    def read_file(self,filename,database):

        articles_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename,'rU',encoding='utf-8') 
                #fd = open(filename,'rU',encoding="ISO-8859-1") 
            else:
                fd = sys.stdin
            wline = Biblio_line()
            for line in fd.readlines():
                if line == "EN":
                    break
                line = line.strip('\ufeff') 
                line = line.strip('\n') # removes \n
                wline.parse_line(line, database)
                if line.startswith("ER"):
                    articles_list.append( wline )
                    wline = Biblio_line()

            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")
        self.articles   = articles_list

## ##################################################
## ##################################################
## ##################################################

class Article:

    def __init__(self):
        self.id          = 0
        self.firstAU     = ""
        self.pubdate     = ""       
        self.year        = 0
        self.journal     = ""
        self.volume      = ""
        self.page        = ""
        self.doi         = ""
        self.pubtype     = ""
        self.doctype     = ""
        self.language    = ""
        self.times_cited = 0
        self.title       = ""
        self.uniqueID    = ""
 
        self.articles      = []      # liste d'articles


    def read_file(self,filename):
        """
        Lecture des articles
        """
        articles_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename, encoding='utf8')
            else:
                fd = sys.stdin
            # read
            aux = 0
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    aline = Article()
                    aline.id = int(s[0])
                    if(len(s)>1): aline.firstAU = s[1]
                    if(len(s)>2): aline.year = int(s[2]) 
                    if(len(s)>3): aline.journal = s[3] 
                    if(len(s)>4): aline.volume = s[4] 
                    if(len(s)>5): aline.page = s[5] 
                    if(len(s)>6): aline.doi  = s[6]
                    if(len(s)>7): aline.pubtype = s[7]
                    if(len(s)>8): aline.doctype = s[8]
                    if(len(s)>9): aline.language = s[9]
                    if(len(s)>10): 
                        try: aline.times_cited = int('0'+s[10])
                        except: aline.times_cited = 0
                    if(len(s)>11): aline.title = s[11]
                    if(len(s)>12): aline.pubdate = s[12]
                    if(len(s)>13): aline.uniqueID = s[13]

                    if len(aline.journal) == 0:
                      aline.journal='%s - %s %d, %s ' % (aline.pubtype, aline.firstAU, aline.year, aline.title)
   
                    articles_list.append( aline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.articles   = articles_list

## ##################################################
## ##################################################
## ##################################################

class Author:

    def __init__(self):
        self.id     = 0
        self.rank   = 0       
        self.author = ""
 
        self.authors  = []      # liste 


    def read_file(self,filename):
        """
        Lecture des articles
        """
        alines_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    aline = Author()
                    aline.id = int(s[0])
                    aline.rank = int(s[1])
                    aline.author = s[2]  
                    alines_list.append( aline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.authors   = alines_list

## ##################################################
## ##################################################
## ##################################################

class Country:

    def __init__(self):
        self.id     = 0
        self.rank   = 0       
        self.country = ""
 
        self.countries  = []      # liste 


    def read_file(self,filename):
        """
        Lecture des articles
        """
        clines_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    cline = Country()
                    cline.id = int(s[0])
                    cline.rank = int(s[1])
                    cline.country = s[2].lower().capitalize()  
   
                    clines_list.append( cline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.countries   = clines_list

## ##################################################
## ##################################################
## ##################################################

class City:

    def __init__(self):
        self.id     = 0
        self.rank   = 0       
        self.city = ""
 
        self.cities  = []      # liste 


    def read_file(self,filename):
        """
        Lecture des articles
        """
        clines_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    cline = City()
                    cline.id = int(s[0])
                    cline.rank = int(s[1])
                    cline.city = s[2]  
   
                    clines_list.append( cline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.cities   = clines_list

## ##################################################
## ##################################################
## ##################################################

class Institution:

    def __init__(self):
        self.id     = 0
        self.rank   = 0       
        self.institution = ""
 
        self.institutions  = []      # liste 


    def read_file(self,filename):
        """
        Lecture des articles
        """
        ilines_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    iline = Institution()
                    if len(s)==3:
                      iline.id = int(s[0])
                      iline.rank = int(s[1])
                      iline.institution = s[2].upper()  
   
                      ilines_list.append( iline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.institutions   = ilines_list

## ##################################################
## ##################################################
## ##################################################

class Keyword:

    def __init__(self):
        self.id      = 0
        self.ktype   = ""       
        self.keyword = ""
 
        self.keywords  = []      # liste 


    def read_file(self,filename):
        """
        Lecture des articles
        """
        klines_list = []
        breakpoint()
        try:
            # open
            if filename != 'st.lower().capitalize()din':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line == "DE"):
                    databaseLine = line.split("; ")
                    for keyword in databaseLine:
                        kline = Keyword()
                        kline.keyword = keyword
                        klines_list.append( kline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.keywords   = klines_list

## ##################################################
## ##################################################
## ##################################################

class Ref:

    def __init__(self):
        self.id      = 0
        self.firstAU = ""       
        self.year    = 0
        self.title = ""
        self.DOI     = ""
        self.refs      = []      # liste de refs


    def parse_ref(self, refs):
        """
        parse a ref of the WoS or Scopus format  
        """
        for citation in refs: 
            if citation == "":
                continue 
            citation_array = citation.split(", ")
            title = ""
            for str in citation_array[0:-3]:
                title = title.join(str)
            self.title = title
            self.firstAU = citation_array[-3] 
            self.year = int(citation_array[-2]) 
            self.DOI = citation_array[-1]
            self.refs.append( self )


    
    def read_file(self,filename):
        """
        Lecture des refs
        """
        refs_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename, encoding='utf8')
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip('\n') # removes \n
                if (line == "CR"):
                    citation_line = line[3:].split("; ")
                    parse_ref(citation_line)
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.refs   = refs_list

## ##################################################
## ##################################################
## ##################################################

class Subject:

    def __init__(self):
        self.id      = 0
        self.subject = ""       
 
        self.subjects  = []      # liste 


    def read_file(self,filename):
        """
        Lecture des articles
        """
        slines_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    sline = Subject()
                    sline.id = int(s[0])
                    sline.subject = s[1] 
   
                    slines_list.append( sline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.subjects   = slines_list

## ##################################################
## ##################################################
## ##################################################

class Abstract:

    def __init__(self):
        self.id      = 0
        self.abstract = ""       
 
        self.abstracts  = []      # liste 


    def read_file(self,filename):
        #"
        #Lecture des abstract
        #"
        alines_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    aline = Abstract()
                    aline.id = int(s[0])
                    aline.abstract = s[1] 
   
                    alines_list.append( aline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.abstracts   = alines_list

## ##################################################
## ##################################################
## ##################################################

class Labo:

    def __init__(self):
        self.id   = 0      
        self.labo = ""
 
        self.labos  = []      # liste 


    def read_file(self,filename):
        """
        Lecture des labos
        """
        llines_list = []
        try:
            # open
            if filename != 'stdin':
                fd = open(filename)
            else:
                fd = sys.stdin
            # read
            for line in fd.readlines():
                line = line.strip() # removes \n
                if (line != ""):
                    s = line.split("\t")
                    lline = Labo()
                    if len(s)==2:
                      lline.id = int(s[0])
                      lline.labo = s[1]
   
                      llines_list.append( lline )
            # close  
            if filename != 'stdin':
                fd.close()
        except IOError:
            print ("file does not exist")

        self.labos   = llines_list

## ##################################################
## ##################################################
## ##################################################
    
## ##################################################
## ##################################################
## ##################################################

if __name__ == "__main__":
    main()

## ##################################################
## ##################################################
## ##################################################

