#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import Documents
from .models import Global
# from .database import DB

from .ri_vetorial.documento import Documento
from .ri_vetorial.colecao import Colecao, sort_dic
from .ri_vetorial.consulta import Consulta
from .ri_vetorial.tokens import archive as archive
from .ri_vetorial.tokens.files import Read

import json


class Connection(object):
    def __init__(self):
        pass

    def startColecao(self):
        colecao = Colecao()
        self.verificaQtDocumentos()

        colecao_bd = Global.objects.values().distinct()[0]

        colecao.tokens = json.loads(colecao_bd['words'])
        colecao.idf = json.loads(colecao_bd['idf'])
        colecao.listTermosColecao = sorted(list(colecao.tokens.keys()))
        colecao.qtDocumentos = len(Documents.objects.values('name').distinct())
        colecao.qtTermos = len(colecao.listTermosColecao)

        if colecao.qtDocumentos != 0:
            colecao.listDocuments = list(Documents.objects.values('name').distinct()[0].values())
        colecao.listDocuments = self.get_documents()

        colecao.qtToken = colecao_bd['qtTokens']
        colecao.qtStopword = colecao_bd['qtStopwords']
        colecao.qtAdverbio = colecao_bd['qtAdverbios']

        colecao.qtTermoDocumento = json.loads(colecao_bd['qtDocument'])

        colecao.algoritmo = {
            'tf': 'DoubleNormalization',  # RawFrequency, DoubleNormalization, LogNormalization
            'idf': 'InverseFrequency',  # InverseFrequency, InverseFrequencySmooth
            'tfidf': 'TFIDF'}  # TFIDF

        return colecao

    def startSearch(self, query):
        return Consulta(query)

    def get_documents(self):
        docs = Documents.objects.values(
            'name', 'text', 'tokens',
            'qtStopwords', 'qtStopwordsTotal',
            'qtAdverbios', 'qtAdverbiosTotal',
            'qtToken', 'qtTokenTotal',
            'tf', 'tfLog', 'tfDouble', 'max').distinct()

        temp = []
        for doc in docs:
            d = Documento(doc['name'], doc['text'])
            print(d.nome)
            d.tokens = json.loads(doc['tokens'])
            d.qtStopword = doc['qtStopwords']
            d.qtStopwordTotal = doc['qtStopwordsTotal']
            d.qtAdverbio = doc['qtAdverbios']
            d.qtAdverbioTotal = doc['qtAdverbiosTotal']
            d.qtToken = doc['qtToken']
            d.qtTokenTotal = doc['qtTokenTotal']

            d.termoMaiorFrequencia = doc['max']
            d.listaTermos = sorted(list(d.tokens.keys()))

            d.tf = json.loads(doc['tf'])
            d.logNormalization = json.loads(doc['tfLog'])
            d.doubleNormalization = json.loads(doc['tfDouble'])

            temp.append(d)
        return temp

    def verificaQtDocumentos(self):
        qtDocument = len(Documents.objects.values('name').distinct())
        # qtDocumentBd = Global.objects.values('qtDocument').distinct()[0]['qtDocument']

        if qtDocument == 0:
            print('Atualizando BD, quantidade de documentos não corresponde...')
            # DB().update_global_all()

        return qtDocument

    def readFile(self, name, path):
        return Read(name, path).text
