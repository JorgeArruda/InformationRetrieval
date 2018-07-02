#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import Documents
from .models import Global
from .ri_vetorial.tokens import archive as archive
from .colecao_to_bd import Connection
import json


class DB(object):
    def __init__(self):
        pass

    def update_global_idf(self):
        "Atualiza o idf da coleção"
        colecao = Connection().startColecao()

        idf = json.dumps(colecao.updateIdf(), ensure_ascii=False)
        # print('>>>>>>> idf', idf)

        id = Global.objects.values('id').distinct()[0]['id']
        document_edit = Global.objects.get(id=id)  # object to update
        document_edit.idf = idf  # update idf
        document_edit.save()  # save object

        return True

    def update_global_remove(self, nameDocument=''):
        "Atualiza a frequencia global de palavras removendo os tokens do documento a ser excluido"
        if nameDocument == '':
            print('\n\tNenhum documento excluido, nome do documento vazio.')
            return False

        document = Documents.objects.values('tokens', 'qtStopwordsTotal', 'qtAdverbiosTotal', 'qtTokenTotal').filter(name=nameDocument)

        if (len(document) == 0):
            print('\n\tNenhum documento excluido, nome inexistente.')
            return False

        tokens = json.loads(document[0]['tokens'])

        allwords = json.loads(Global.objects.values('words').distinct()[0]['words'])
        qt_document = json.loads(Global.objects.values('qtDocument').distinct()[0]['qtDocument'])
        qt_stopwords = int(Global.objects.values('qtStopwords').distinct()[0]['qtStopwords']) - int(document[0]['qtStopwordsTotal'])
        qt_adverbios = int(Global.objects.values('qtAdverbios').distinct()[0]['qtAdverbios']) - int(document[0]['qtAdverbiosTotal'])
        qt_tokens = int(Global.objects.values('qtTokens').distinct()[0]['qtTokens']) - int(document[0]['qtTokenTotal'])

        for key in tokens:
            if (key in allwords):
                allwords[key] -= tokens[key]
                if (allwords[key] == 0):
                    allwords.pop(key)

            if (key in qt_document):
                qt_document[key] -= 1
                if (qt_document[key] == 0):
                    qt_document.pop(key)

        # print('\nallwords from global >>', allwords)
        Global(
            id=1, words=json.dumps(allwords, ensure_ascii=False),
            qtStopwords=qt_stopwords, qtAdverbios=qt_adverbios,
            qtTokens=qt_tokens,
            qtDocument=json.dumps(qt_document, ensure_ascii=False)).save()
        return True

    def update_global_insert(self, nameDocument=''):
        "Atualiza a frequencia global de palavras adicionado os tokens do documento a ser salvo"
        if (nameDocument == ''):
            print('\n\tNenhum documento salvo, nome do documento vazio.')
            return False

        document = Documents.objects.values('tokens', 'qtStopwordsTotal', 'qtAdverbiosTotal', 'qtTokenTotal').filter(name=nameDocument)

        if (len(document) == 0):
            print('\n\tNenhum documento salvo, nome inexistente.')
            return False

        tokens = json.loads(document[0]['tokens'])

        allwords = json.loads(Global.objects.values('words').distinct()[0]['words'])
        qt_document = json.loads(Global.objects.values('qtDocument').distinct()[0]['qtDocument'])
        qt_stopwords = int(Global.objects.values('qtStopwords').distinct()[0]['qtStopwords']) + int(document[0]['qtStopwordsTotal'])
        qt_adverbios = int(Global.objects.values('qtAdverbios').distinct()[0]['qtAdverbios']) + int(document[0]['qtAdverbiosTotal'])
        qt_tokens = int(Global.objects.values('qtTokens').distinct()[0]['qtTokens']) + int(document[0]['qtTokenTotal'])

        for key in tokens:
            if (key in allwords):
                allwords[key] += tokens[key]
            else:
                allwords[key] = tokens[key]

            if (key in qt_document):
                qt_document[key] += 1
            else:
                qt_document[key] = 1

        # print('\nallwords from global >>', allwords)
        Global(
            id=1, words=json.dumps(allwords, ensure_ascii=False),
            qtStopwords=qt_stopwords, qtAdverbios=qt_adverbios,
            qtTokens=qt_tokens,
            qtDocument=json.dumps(qt_document, ensure_ascii=False)).save()
        return True

    def update_global_all(self):
        documents = Documents.objects.values('name').distinct()

        Global(
            id=1, words=json.dumps({}, ensure_ascii=False),
            qtStopwords=0, qtAdverbios=0, qtTokens=0,
            qtDocument=json.dumps({}, ensure_ascii=False),
            idf=json.dumps({}, ensure_ascii=False)).save()
        for doc in documents:
            self.update_global_insert(doc['name'])

        self.update_global_idf()
        return True

    def remove_document(self, filename):
        document = Documents.objects.values('name').filter(name=filename)
        if (len(document) == 0):
            return False
        document = Documents.objects.get(name=filename)
        document.delete()

        self.update_global_all()
        return True

    def insert_document(self, filename, texto):
        colecao = Connection().startColecao()
        doc = colecao.addDocumento(filename, texto)
        doc.processar(colecao)
        # Calcula a frequencia de palavras no documento
        # token = archive.get_frequency(archive.get_tokens(texto))
        # Remove e conta as stopwords removidas
        # token = archive.remove_stopwords(token)
        # Calcula a tf ajustada pelo tamanho do documento
        tf_adjusted = doc.tf
        tf_log = doc.logNormalization  # archive.get_tfLog(token['tokens'])
        tf_double = doc.doubleNormalization  # archive.get_tfDouble(token['tokens'], token['max'])
        # Salva o novo documento no db
        Documents(
            name=filename, text=texto,
            tokens=json.dumps(doc.tokens, ensure_ascii=False),
            tf=json.dumps(tf_adjusted, ensure_ascii=False),
            tfLog=json.dumps(tf_log, ensure_ascii=False),
            tfDouble=json.dumps(tf_double, ensure_ascii=False),
            qtStopwords=doc.qtStopword,
            qtStopwordsTotal=doc.qtStopwordTotal,
            qtAdverbios=doc.qtAdverbio,
            qtAdverbiosTotal=doc.qtAdverbioTotal,
            qtToken=doc.qtToken, qtTokenTotal=doc.qtTokenTotal,
            max=doc.termoMaiorFrequencia).save()

        # # Salva a frequencia global atualizada
        self.update_global_insert(filename)
        self.update_global_idf()
        # Global(id=1, words=json.dumps(words, ensure_ascii=False)).save()
