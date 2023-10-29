"""Multiple file Autocad data extraction"""
"""Python script for extracting information from Autocad block attributes in multiple documents."""

import os
from os import listdir
import pandas as pd
##pip install ezdxf
import ezdxf

#Specify folder where you have dxf files
cartella="relativepath/fodler"
for nomefile in os.listdir(cartella):
  print(nomefile)
  doc = ezdxf.readfile("{}/{}".format(cartella, nomefile))

#Function that you need to cycle over each file
#NUMEROARTICOLO is a user-defined parameter to filter specific autocad blocks
user_defined_dictionary={}

def extract_attr_dxf(cartella, nomefile):
    doc = ezdxf.readfile("{}/{}".format(cartella, nomefile))
    modelspace = doc.modelspace()
    for n in modelspace:
        if n.dxftype()=="INSERT":
            articolo={}
            if n.has_attrib("NUMEROARTICOLO")==True:
                for attrib in n.attribs:
                    articolo[attrib.dxf.tag]=attrib.dxf.text
                user_defined_dictionary[articolo["NUMEROARTICOLO"]]=articolo

for nomefile in os.listdir(cartella):
  if nomefile.endswith(".dxf"):
    extract_attr_dxf(cartella,nomefile)

#Enjoy