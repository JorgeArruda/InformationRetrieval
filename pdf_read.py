#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pdftotext

def files_folder(path):
    if type(path) != str:
        return "Erro, argument path != string"
    files = os.listdir(path)
    documents = {}
    for file in files:
        pdf = pdftotext.PDF(open(path+file, "rb"))
        full_text = ''
        for page in pdf:
            full_text = full_text+page
        documents[file] = full_text           
    return documents

def file(name):    
    if type(name) != str:
        return "Erro, argument name != string"
    pdf = pdftotext.PDF(open(name, "rb"))
    full_text = ''
    for page in pdf:
        full_text = full_text+page
    return full_text