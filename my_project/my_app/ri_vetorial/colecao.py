#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from operator import itemgetter
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
        self.ifsmooth = {}
        self.ifmax = {}
        self.ifprobabilistic = {}

        self.qtToken = 0
        self.qtStopword = 0
        self.qtAdverbio = 0

        self.qtTermoDocumento = {}
        self.algoritmo = {'tf': 'DoubleNormalization',  # RawFrequency, DoubleNormalization, LogNormalization
                          'idf': 'InverseFrequencySmooth',  # InverseFrequency, InverseFrequencySmooth
                          'tfidf': 'TFIDF'}  # TFIDF

    def __str__(self):
        return 'qtDocumentos: '+str(self.qtDocumentos)+', qtWord: '+\
            str(self.qtToken)+', qtStopword: '+str(self.qtStopword)+\
            ', qtAdverbio: '+str(self.qtAdverbio)

    def addDocumento(self, nome, text):
        posicao = self.pesquisarDocumento(nome)
        if posicao == -1:
            doc = Documento(nome, text)
            doc.remove_stopwords()
            doc.processar(self)

            self.qtToken += doc.qtTokenTotal
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
        InverseFrequency = idf_class.InverseFrequency()
        IFSmooth = idf_class.InverseFrequencySmooth()
        IFMax = idf_class.InverseFrequencyMax()
        IFProbabilistic = idf_class.InverseFrequencyProbabilistic()

        self.idf = {}
        self.ifsmooth = {}
        self.ifmax = {}
        self.ifprobabilistic = {}

        qt = self.qtDocumentos  # Quantidade total de documentos da coleção
        qtMAX = 0
        if self.qtTermoDocumento:
            qtMAX = sort_dic(self.qtTermoDocumento, 1, True)[0][1]
        # print('Colecao().updateidf() qtMAX = ', qtMAX)
        for key in self.qtTermoDocumento:
            self.idf[key] = InverseFrequency.calcPeso(qt, self.qtTermoDocumento[key])
            self.ifsmooth[key] = IFSmooth.calcPeso(qt, self.qtTermoDocumento[key])
            self.ifmax[key] = IFMax.calcPeso(qtMAX, self.qtTermoDocumento[key])
            self.ifprobabilistic[key] = IFProbabilistic.calcPeso(qt, self.qtTermoDocumento[key])
        return self.idf

    def instanciar(self, origem, nome):
        try:
            return getattr(origem, nome)()
        except AttributeError:
            print('Error, a classe %s não existe' % (nome))

    def calcular_similaridade(self, consulta, strategyTF='DoubleNormalization', strategyIDF='InverseFrequencySmooth'):
        # idf = self.idf
        docs = self.listDocuments
        print('calcular_similaridade | strategyTF: ', strategyTF, '  strategyIDF: ', strategyIDF)
        # words = self.listTermosColecao
        result = {}
        for doc in docs:
            sum_q = sum_d = similaridade = 0.0
            for termo in doc.tf:
                idf = self.get_idf(termo, strategyIDF)
                tf = self.get_tf(termo, doc, strategyTF)

                sum_d += ((tf * idf)**2)**(0.5)

            for termo in consulta.tokens:
                idf = self.get_idf(termo, strategyIDF)
                tf = self.get_tf(termo, consulta, strategyTF)

                sum_q += ((tf * idf)**2)**(0.5)

            for word in consulta.tokens:
                doc_weight = 0.0
                idf = self.get_idf(termo, strategyIDF)
                if word in doc.listaTermos:
                    doc_weight = doc.tf[word] * idf
                similaridade += consulta.tokens[word] * (idf * doc_weight)
            if sum_d == 0.0 or sum_q == 0.0:
                similaridade = 0.0
            else:
                similaridade = similaridade / (sum_q * sum_d)
            if similaridade > 0.0:
                result[doc.nome] = similaridade
        print('... colecao()calcular_similaridade()  result: ', result)
        return sort_dic(result, 1, True)

    def get_idf(self, termo, strategy='InverseFrequencySmooth'):
        'Escolhe qual idf da coleção usar'
        idf = 0.0
        if termo in self.idf:
            if strategy == 'InverseFrequencySmooth':
                idf = self.ifsmooth[termo]
            elif strategy == 'InverseFrequency':
                idf = self.idf[termo]
            elif strategy == 'InverseFrequencyMax':
                idf = self.ifmax[termo]
            elif strategy == 'InverseFrequencyProbabilistic':
                idf = self.ifprobabilistic[termo]
        return idf

    def get_tf(self, termo, doc, strategy='DoubleNormalization'):
        'Escolhe qual tf de um documento ou consulta usar'
        tf = 0.0
        if termo in doc.tf:
            if strategy == 'DoubleNormalization':
                tf = doc.doubleNormalization[termo]
            elif strategy == 'RawFrequency':
                tf = doc.tf[termo]
            elif strategy == 'LogNormalization':
                tf = doc.logNormalization[termo]
        return tf


def sort_dic(dic, indice=0, reverse=False):
    return sorted(dic.items(), key=itemgetter(indice), reverse=reverse)
