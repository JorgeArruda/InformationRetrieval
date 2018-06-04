#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import Documents
from .models import Global

import json

import my_app.ri_vetorial.archive as archive


def update_global_idf():
    "Atualiza o idf da coleção"

    qt_document = json.loads(Global.objects.values('qtDocument').distinct()[0]['qtDocument'])
    qt_total = len(Documents.objects.values('name').distinct())
    colecao = Global.objects.values().distinct()[0]

    colecao['idf'] = json.dumps(archive.get_idf(qt_document, qt_total), ensure_ascii=False)

    document_edit = Global.objects.get(id=colecao['id'])  # object to update
    document_edit.idf = colecao['idf']  # update idf
    document_edit.save()  # save object

    return True


def update_global_remove(nameDocument=''):
    "Atualiza a frequencia global de palavras removendo os tokens do \
    documento a ser excluido"
    if (nameDocument == ''):
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
    Global(id=1, words=json.dumps(allwords, ensure_ascii=False),
           qtStopwords=qt_stopwords, qtAdverbios=qt_adverbios,
           qtTokens=qt_tokens,
           qtDocument=json.dumps(qt_document, ensure_ascii=False)).save()
    return True


def update_global_insert(nameDocument=''):
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
    Global(id=1, words=json.dumps(allwords, ensure_ascii=False),
           qtStopwords=qt_stopwords, qtAdverbios=qt_adverbios,
           qtTokens=qt_tokens,
           qtDocument=json.dumps(qt_document, ensure_ascii=False)).save()
    return True


def update_global_all():
    documents = Documents.objects.values('name').distinct()

    Global(id=1, words=json.dumps({}, ensure_ascii=False),
           qtStopwords=0, qtAdverbios=0, qtTokens=0,
           qtDocument=json.dumps({}, ensure_ascii=False),
           idf=json.dumps({}, ensure_ascii=False)).save()
    for doc in documents:
        update_global_insert(doc['name'])

    update_global_idf()
    return True


def remove_document(filename):
    document = Documents.objects.values('name').filter(name=filename)
    if (len(document) == 0):
        return False
    document = Documents.objects.get(name=filename)
    document.delete()

    update_global_all()
    return True


def insert_document(filename, texto):
    # Calcula a frequencia de palavras no documento
    token = archive.get_frequency(archive.get_tokens(texto))
    # print("TOKENS ",token)

    # Remove e conta as stopwords removidas
    token = archive.remove_stopwords(token)
    # Calcula a tf ajustada pelo tamanho do documento
    tf_adjusted = archive.get_tf(token['tokens'], token['qt_tok_total'])
    tf_log = archive.get_tfLog(token['tokens'])
    tf_double = archive.get_tfDouble(token['tokens'], token['max'])

    # Salva o novo documento no db
    Documents(name=filename, text=texto, tokens=json.dumps(token['tokens'], ensure_ascii=False),
              tf=json.dumps(tf_adjusted, ensure_ascii=False),
              tfLog=json.dumps(tf_log, ensure_ascii=False),
              tfDouble=json.dumps(tf_double, ensure_ascii=False),
              qtStopwords=token['qt_stopwords'], qtStopwordsTotal=token['qt_stopwords_total'],
              qtAdverbios=token['qt_adverbios'], qtAdverbiosTotal=token['qt_adverbios_total'],
              qtToken=token['qt_tok'], qtTokenTotal=token['qt_tok_total'], max=token['max']).save()

    # # Salva a frequencia global atualizada
    update_global_insert(filename)
    update_global_idf()
    # Global(id=1, words=json.dumps(words, ensure_ascii=False)).save()
