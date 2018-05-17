#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import codecs

def files_folder(path):
    if type(path) != str:
        return "Erro, argument path != string"
    files = os.listdir(path)
    documents = {}
    for file in files:
        documents[file] = BeautifulSoup( codecs.open( path+file, 'r').read() , 'lxml').get_text()           
    return documents

def file(name):    
    if type(name) != str:
        return "Erro, argument name != string"
    return BeautifulSoup( codecs.open(name, 'r').read() , 'lxml').get_text()