#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .frequency import term_frequency as tf_class
    from .frequency import inverse_frequency as idf_class
    from .frequency import tf_idf as tfidf_class

    from .tokens.lex import tokenize
    from .tokens.archive import remove_stopwords
    from .termo import TermoColecao, Termo
except ImportError:
    from tokens.lex import tokenize
    from tokens.archive import remove_stopwords
    from termo import TermoColecao, Termo


class Documento(object):
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
        self.listTermosProcessados = []
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

    def processar(self, colecao, listaDocumentos, strategyTF, strategyIDF, strategyTFIDF='TFIDF'):
        strategyTF = self.instanciar(tf_class, strategyTF)
        strategyIDF = self.instanciar(idf_class, strategyIDF)
        strategyTFIDF = self.instanciar(tfidf_class, strategyTFIDF)

        for word in self.tokens:
            termo = Termo()
            self.word = word
            self.frequency = self.tokens[word]
            termo.tf = strategyTF.calcularPeso(termo, self)
            termo.idf = idf = strategyIDF.calcularPeso(termo, listaDocumentos)
            termo.tfIdf = termo.tf * termo.idf

            colecao.addTermo(termo, idf)
            self.listTermosProcessados.append(termo)

    def instanciar(self, origem, strategy):
        try:
            return getattr(origem, strategy)()
        except AttributeError:
            print('Error, a classe %s não existe' % (strategy))
    # def retirarStopWords()
    # def buscarTermo()
