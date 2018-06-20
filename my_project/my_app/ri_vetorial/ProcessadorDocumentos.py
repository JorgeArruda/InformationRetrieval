#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    import term_frequency as tf_class
    import inverse_frequency as idf_class
    import tf_idf as tfidf_class
    from .term import Termo
except ImportError:
    import term_frequency as tf_class
    import inverse_frequency as idf_class
    import tf_idf as tfidf_class
    from term import Termo


class ProcessadorDocumentos(object):
    def __init__(self, strategyTF, strategyIDF, strategyTFIDF='TFIDF'):
        self.strategyTF = self.instanciar(tf_class, strategyTF)
        self.strategyIDF = self.instanciar(idf_class, strategyIDF)
        self.strategyTFIDF = self.instanciar(tfidf_class, strategyTFIDF)

        # termo = Termo()
        # termo.frequency = 20
        # print(self.strategyTF)

    def processar(self, documento, listaDocumentos):
        listaTermosProcessados = documento.listaTermosProcessados
        for termo in listaTermosProcessados:
            termo.tf = self.strategyTF.calcularPeso(termo, documento)
            termo.idf = idf = self.strategyIDF.calcularPeso(termo, listaDocumentos)
            # Colecao.addTermo(termo, idf)
            termo.tfIdf = termo.tf * termo.idf

    def instanciar(self, origem, strategy):
        try:
            return getattr(origem, strategy)()
        except AttributeError:
            print('Error, a classe %s não existe' % (strategy))
