#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .lex import tokenize
    from .archive import remove_stopwords
except ImportError:
    from lex import tokenize
    from archive import remove_stopwords


class Document(object):
    def __init__(self):
        self.nome = ''
        self.text = ' '
        self.qtWord = 0
        self.qtWordTotal = 0
        self.qtStopword = 0
        self.qtStopwordTotal = 0
        self.qtAdverbio = 0
        self.qtAdverbioTotal = 0
        self.termoMaiorFrequencia = 0
        # self.listTermosProcessados = []
        self.listaTermos = []
        self.tokens = {}

    def get_tokens(self, language='portuguese'):
        return tokenize(self.text, language)

    def remove_stopwords(self):
        result = remove_stopwords(self.get_tokens())
        self.qtWord = result['qt_tok'] - result['qt_stopwords'] - result['qt_adverbios']
        self.qtWordTotal = result['qt_tok_total'] - result['qt_stopwords'] - result['qt_stopwords_total']
        self.qtStopword = result['qt_stopwords']
        self.qtStopwordTotal = result['qt_stopwords_total']
        self.qtAdverbio = result['qt_adverbios']
        self.qtAdverbioTotal = result['qt_adverbios_total']

        self.termoMaiorFrequencia = result['max']

        self.tokens = result['tokens']
        self.listaTermos = sorted(list(self.tokens.keys()))

    # def retirarStopWords()
    # def buscarTermo()
