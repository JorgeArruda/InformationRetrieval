#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from docx import Document   # Read docx
import pdftotext    # Read pdf
from bs4 import BeautifulSoup   # Read html
import codecs   # Read html
from PIL import Image   # Importando o módulo para abrir a imagem no script
from pytesseract import image_to_string   # Módulo para a utilização de OCR


class Read(object):
    def html(self, name):
        if type(name) != str:
            return "Erro, argument name != string"
        return BeautifulSoup(codecs.open(name, 'r').read(), 'lxml').get_text()

    def pdf(self, name):
        if type(name) != str:
            return "Erro, argument name != string"
        pdf = pdftotext.PDF(open(name, "rb"))
        full_text = ''
        for page in pdf:
            full_text = full_text+page
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
