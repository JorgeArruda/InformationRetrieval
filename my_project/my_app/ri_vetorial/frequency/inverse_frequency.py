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

    def calcPeso(self, termo, listaDocumentos):
        qtDocumentosTermo = self.getQtDocumentosTermo(termo.word, listaDocumentos)
        qtDoc = len(listaDocumentos)

        return math.log2(qtDoc / qtDocumentosTermo)


class InverseFrequencySmooth(object):
    def __init__(self):
        pass


class InverseFrequencyMax(object):
    def __init__(self):
        pass


class InverseFrequencyProbabilistic(object):
    def __init__(self):
        pass
