#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import math


class AbstractIDF(ABC):

    @abstractmethod
    def calcPeso(self, termo, listaDocumentos):
        pass

    def getQtDocumentosTermo(self, word, listaDocumentos):
        qtDocumentos = 0

        for document in listaDocumentos:
            for termo in document.listaTermosProcessados:
                if termo == word:
                    qtDocumentos += 1
        return qtDocumentos


class InverseFrequency(AbstractIDF):
    def __init__(self):
        pass

    def calcPeso(self, qtDoc, qtDocTermo):
        return math.log2(qtDoc / qtDocTermo)


class InverseFrequencySmooth(object):
    def __init__(self):
        pass

    def calcPeso(self, qtDoc, qtDocTermo):
        return math.log2(1 + (qtDoc / qtDocTermo))


class InverseFrequencyMax(object):
    def __init__(self):
        pass

    def calcPeso(self, qtDoc, qtDocTermo):
        "qtDoc deve ser a freq max entre os termos nos documentos da coleção"
        return math.log2(1 + (qtDoc / (1 + qtDocTermo)))


class InverseFrequencyProbabilistic(object):
    def __init__(self):
        pass

    def calcPeso(self, qtDoc, qtDocTermo):
        return math.log2((1 + qtDoc - qtDocTermo) / qtDocTermo)
