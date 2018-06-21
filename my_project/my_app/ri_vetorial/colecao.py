#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .termo import TermoColecao, Termo
    from .frequency import inverse_frequency as idf_class
    from .documento import Documento
except ImportError:
    from termo import TermoColecao, Termo
    from documento import Documento
import math


class Colecao(object):
    def __init__(self):
        self.qtDocumentos = 0
        self.listTermosColecao = []
        self.listDocuments = []
        self.tokens = {}
        self.idf = {}

        self.qtWord = 0
        self.qtStopword = 0
        self.qtAdverbio = 0

        self.qtTermoDocumento = {}
        self.algoritmo = {'tf': 'RawFrequency',  # RawFrequency, DoubleNormalization, LogNormalization
                          'idf': 'InverseFrequency',  # InverseFrequency
                          'tfidf': 'TFIDF'}  # TFIDF

    def addDocumento(self, nome, text):
        posicao = self.pesquisarDocumento(nome)
        if posicao == -1:
            doc = Documento()
            doc.nome = nome
            doc.text = text
            doc.remove_stopwords()
            doc.processar(self, self.listDocuments,
                          self.algoritmo['tf'],
                          self.algoritmo['idf'],
                          self.algoritmo['tfidf'])

            self.listDocuments.append(doc)
            self.qtDocumentos += 1
            return doc
        else:
            print('O documento %s já está na coleção' % (nome))
            return -1

    def pesquisarWord(self, word):
        if word in self.listTermosColecao:
            return self.listTermosColecao.index(word)
        return -1

    def pesquisarDocumento(self, nome):
        for doc in self.listDocuments:
            if nome == doc.nome:
                return self.listDocuments.index(doc)
        return -1

    def updateIdf(self):
        strategyIDF = self.instanciar(idf_class, self.algoritmo['idf'])
        self.idf = {}
        for key in self.qtTermoDocumento:
            self.idf[key] = strategyIDF.calcPeso(self.qtDocumentos, self.qtTermoDocumento[key])
        return self.idf

    def instanciar(self, origem, nome):
        try:
            return getattr(origem, nome)()
        except AttributeError:
            print('Error, a classe %s não existe' % (nome))
