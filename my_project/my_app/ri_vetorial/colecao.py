#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .termo import TermoColecao, Termo
    from .documento import Documento
except ImportError:
    from termo import TermoColecao, Termo
    from documento import Documento


class Colecao(object):
    def __init__(self):
        self.qtDocumentos = 0
        self.qtTermos = 0
        self.listTermosColecao = []
        self.listDocuments = []
        self.tokens = {}

        self.qtWord = 0
        self.qtStopword = 0
        self.qtAdverbio = 0

        self.algoritmo = {'tf': 'RawFrequency',  # RawFrequency, DoubleNormalization, LogNormalization
                          'idf': 'InverseFrequency',  # InverseFrequency
                          'tfidf': 'TFIDF'}  # TFIDF

    def incQtdDocumentos(self):
        self.qtDocumentos += 1

    def incQtdTermos(self):
        self.qtTermos += 1

    def addTermo(self, termo, idf):
        posicao = self.pesquisarWord(termo.word)
        if posicao == -1:
            self.listTermosColecao.append(TermoColecao(termo.word, idf))
            self.incQtdTermos()
        else:
            self.listTermosColecao[posicao].idf = idf

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
            self.incQtdDocumentos()
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
