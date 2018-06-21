#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from docx import Document   # Read docx
# import pdftotext    # Read pdf
from tika import parser
from bs4 import BeautifulSoup   # Read html
import codecs   # Read html
from PIL import Image   # Importando o módulo para abrir a imagem no script
from pytesseract import image_to_string   # Módulo para a utilização de OCR


class Read(object):
    def __init__(self, name, path='/'):
        self.text = ' '
        if type(path) != str:
            print("Erro, argument path != string")
        archive_type = name.split(".")[-1]
        try:
            if (archive_type == "html"):
                self.text = self.html(path+name)
            elif (archive_type == "pdf"):
                self.text = self.pdf(path+name)
            elif (archive_type == "docx"):
                self.text = self.docx(path+name)
            elif ((archive_type == "jpg") | (archive_type == "png")):
                self.text = self.image(path+name)
        except FileNotFoundError:
            print("No such file or directory: ", path+name)

    def html(self, name):
        if type(name) != str:
            return "Erro, argument name != string"
        return BeautifulSoup(codecs.open(name, 'r').read(), 'lxml').get_text()

    def pdf(self, name):
        if type(name) != str:
            return "Erro, argument name != string"
        # pdf = pdftotext.PDF(open(name, "rb"))
        # full_text = ''
        # for page in pdf:
        #     full_text = full_text+page

        pdf = parser.from_file(name)
        full_text = pdf['content']

        return full_text

    def docx(self, name):
        if type(name) != str:
            return "Erro, argument name != string"
        text = Document(name)
        full_text = ''
        for p in text.paragraphs:
            full_text = full_text+p.text
        return full_text

    def image(self, name):
        if type(name) != str:
            return "Erro, argument name != string"
        # eng = english and por = portuguese
        return image_to_string(Image.open(name), lang='por')
