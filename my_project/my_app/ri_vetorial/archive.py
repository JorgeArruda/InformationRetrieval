#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Importando arquivos
import my_app.ri_vetorial.lex as lex
import my_app.ri_vetorial.ocr as ocr
import my_app.ri_vetorial.pdf_read as pdf_read
import my_app.ri_vetorial.docx_read as docx_read
import my_app.ri_vetorial.html_read as html_read
from operator import itemgetter

def sort_dic(dic, indice=0):
    return sorted(dic.items(), key=itemgetter(indice))

def get_text(name, path = '/'):
    if type(path) != str:
        return "Erro, argument path != string"
    archive_type = name.split(".")[-1]
    try:
        if (archive_type == "html"):
            return html_read.file(path+name)
        elif (archive_type == "pdf"):
            return pdf_read.file(path+name)
        elif (archive_type == "docx"):
            return docx_read.file(path+name)
        elif ((archive_type == "jpg") | (archive_type == "png")):
            return ocr.file(path+name)
        else:
            return ' '
    except FileNotFoundError:
       print("No such file or directory: ",path+name)
       return ' '

def get_tokens(text, language='portuguese'):
    if type(text) != str:
        return "Erro, argument text != string"
    return lex.tokenize(text, language)

def get_frequency(listTokens, frequencyWord):
        "Vare a lista de tokens do documento, retorna a frequência. Incrementa também a frequência global. return (frequencyDocument, frequencyWord)"

        frequencyDocument = {}
        for token in listTokens:
            print(token)
            if token in frequencyWord:
                frequencyWord[ token ]+=1
            else:
                frequencyWord[ token ]=1

            if token in frequencyDocument:
                frequencyDocument[ token ]+=1
            else:
                frequencyDocument[ token ]=1
        
        return (dict(sort_dic(frequencyDocument)), dict(sort_dic(frequencyWord)))

def get_frequency2(listTokens, frequencyWord):
        "Vare a lista de tokens do documento, retorna a frequência. Incrementa também a frequência global. return (frequencyDocument, frequencyWord)"
        frequencyDocument = {}
        # if type(frequencyWord)=='list':
        for token in listTokens:
            if token in frequencyWord:
                frequencyWord[ token ]+=1
            else:
                frequencyWord[ token ]=1

            if token in frequencyDocument:
                frequencyDocument[ token ]+=1
            else:
                frequencyDocument[ token ]=1
        
        return (dict(sort_dic(frequencyDocument)), frequencyWord)
            
if __name__ =="__main__d":
    get_text("jkak.pdf")
