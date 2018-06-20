#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
try:
    from .files import Read
    from .document import Document
except ImportError:
    from files import Read
    from document import Document


class ManipuladorDocumentos(object):
    def __init__(self, filename, fileStopWords, fileAdv):
        self.filename = filename
        self.fileStopWords = fileStopWords
        self.fileAdv = fileAdv

    def carregarArquivo(self, filename, path):
        document = Document()
        document.text = Read(filename, path).text
        document.nome = filename
        document.
