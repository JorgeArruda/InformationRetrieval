#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Importando arquivos
import my_app.lex as lex
import my_app.ocr as ocr
import my_app.pdf_read as pdf_read
import my_app.docx_read as docx_read
import my_app.html_read as html_read

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
        elif (archive_type == "jpg" | archive_type == "png"):
            return ocr.file(path+name)
    except FileNotFoundError:
       print("No such file or directory: ",path+name)

if __name__ =="__main__":
    get_text("jkak.pdf")