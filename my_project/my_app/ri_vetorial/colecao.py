#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .termo import TermoColecao, Termo
    from .frequency import inverse_frequency as idf_class
    from .documento import Documento
except ImportError:
    from termo import TermoColecao, Termo
    from frequency import inverse_frequency as idf_class
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

    def __str__(self):
        return 'qtDocumentos: '+str(self.qtDocumentos)+', qtWord: '+\
            str(self.qtWord)+', qtStopword: '+str(self.qtStopword)+\
            ', qtAdverbio: '+str(self.qtAdverbio)

    def addDocumento(self, nome, text):
        posicao = self.pesquisarDocumento(nome)
        if posicao == -1:
            doc = Documento(nome, text)
            doc.remove_stopwords()
            doc.processar(self)

            self.qtWord += doc.qtWordTotal
            self.qtStopword += doc.qtStopwordTotal
            self.qtAdverbio += doc.qtAdverbioTotal

            self.listDocuments.append(doc)
            self.qtDocumentos += 1
            self.updateIdf()
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
            if nome == doc:
                return self.listDocuments.index(doc)
        return -1

    def updateIdf(self):
        print('Colecao().updateIdf()')
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
