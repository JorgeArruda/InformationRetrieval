#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    from .term import TermoColecao
except ImportError:
    from term import TermoColecao

class Colecao(object):
    def __init__(self):
        self.qtdDocumentos = 0
        self.qtdTermos = 0
        self.listTermosColecao = []

    def incQtdDocumentos(self):
        self.qtdDocumentos += 1

    def incQtdTermos(self):
        self.qtdTermos += 1

    def addTermo(self, termo, idf):
        posicao = self.pesquisar(termo.word)
        if posicao == -1:
            self.listTermosColecao.append(TermoColecao(termo.word, idf))
            self.incQtdTermos()
        else:
            self.listTermosColecao[posicao].idf = idf

    def pesquisar(self, word):
        if word in self.listTermosColecao:
            return self.listTermosColecao.index(word)
        return -1
