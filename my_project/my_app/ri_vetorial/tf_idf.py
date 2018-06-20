#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
try:
    from .inverse_frequency import InverseFrequency
    from .term_frequency import RawFrequency
except ImportError:
    from inverse_frequency import InverseFrequency
    from term_frequency import RawFrequency


class AbstractTFIDF(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def calcPeso(self, termo, listaDocumentos):
        pass


class TFIDF(AbstractTFIDF):
    def __init__(self, strategyTF=RawFrequency(), strategyIDF=InverseFrequency):
        self.strategyTF = strategyTF
        self.strategyIDF = strategyIDF

    def calcPeso(self, termo, listaDocumentos):
        tf = self.strategyTF.calcPeso(termo, None)
        idf = self.strategyIDF.calcPeso(termo, listaDocumentos)
        return tf * idf
