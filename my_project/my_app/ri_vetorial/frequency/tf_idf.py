#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
try:
    import inverse_frequency as idf
    import term_frequency as tf
except ImportError:
    import inverse_frequency as idf
    import term_frequency as tf


class AbstractTFIDF(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def calcPeso(self, termo, listaDocumentos):
        pass

    def instanciar(self, origem, nome):
        try:
            return getattr(origem, nome)()
        except AttributeError:
            print('Error, a classe %s não existe' % (nome))


class TFIDF(AbstractTFIDF):
    def __init__(self, strategyTF='DoubleNormalization', strategyIDF='InverseFrequencySmooth'):
        self.strategyTF = self.instanciar(tf, strategyTF)
        self.strategyIDF = self.instanciar(idf, strategyIDF)

    def calcPeso(self, termo, listaDocumentos):
        tf = self.strategyTF().calcPeso(termo, None)
        idf = self.strategyIDF().calcPeso(termo, listaDocumentos)
        return tf * idf
