#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import Documents
from .models import Global
# from .database import DB

from .ri_vetorial.colecao import Colecao
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
        colecao.listTermosColecao = sorted(list(colecao.tokens.keys()))

        colecao.qtDocumentos = len(Documents.objects.values('name').distinct())
        colecao.qtTermos = len(colecao.listTermosColecao)

        if colecao.qtDocumentos != 0:
            colecao.listDocuments = list(Documents.objects.values('name').distinct()[0].values())

        colecao.qtWord = colecao_bd['qtTokens']
        colecao.qtStopword = colecao_bd['qtStopwords']
        colecao.qtAdverbio = colecao_bd['qtAdverbios']

        colecao.algoritmo = {
            'tf': 'RawFrequency',  # RawFrequency, DoubleNormalization, LogNormalization
            'idf': 'InverseFrequency',  # InverseFrequency
            'tfidf': 'TFIDF'}  # TFIDF

        return colecao

    def verificaQtDocumentos(self):
        qtDocument = len(Documents.objects.values('name').distinct())
        # qtDocumentBd = Global.objects.values('qtDocument').distinct()[0]['qtDocument']

        if qtDocument == 0:
            print('Atualizando BD, quantidade de documentos não corresponde...')
            # DB().update_global_all()

        return qtDocument

    def readFile(self, name, path):
        return Read(name, path).text
