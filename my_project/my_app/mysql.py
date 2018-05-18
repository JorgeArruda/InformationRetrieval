#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import Documents
from .models import Global

import json
import math

import my_app.ri_vetorial.archive as archive

def update_global_idf():
    "Atualiza o idf global"

    qt_document = json.loads(Global.objects.values('qtDocument').distinct()[0]['qtDocument'])
    gl = Global.objects.values().distinct()[0]
    idf_word = {}
    for key in qt_document :
        qt_total = len(Documents.objects.values('name').distinct())
        idf_word[key] = math.log( qt_total / qt_document[key], 2 )

    gl['idf'] = json.dumps(idf_word, ensure_ascii=False)
    Global(id=1, words=gl['words'],\
        qtStopwords=gl['qtStopwords'], qtAdverbios=gl['qtAdverbios'], qtTokens=gl['qtTokens'],\
        qtDocument=gl['qtDocument'],\
        idf=gl['idf'] ).save()
    return True

def update_tf_normalized( nameDocument ):
    id_doc = Documents.objects.values('id', 'tokens').filter( name=nameDocument )
    if ( len(id_doc) == 0 ):
        print('\n\tNenhum documento alterado, nome inexistente.')
        return False
    tf_normalized = {}
    for token in id_doc[0]['tokens']:
        pass
        
    document_edit = Documents.objects.get( id = id_doc[0]['id'] ) # object to update
    document_edit.tfnormalized = 'New name' # update name
    document_edit.save() # save object
    
    
def update_global_remove( nameDocument = '' ):
    "Atualiza a frequencia global de palavras removendo os tokens do documento a ser excluido"
    if (nameDocument == ''):
        print('\n\tNenhum documento excluido, nome do documento vazio.')
        return False
        
    document = Documents.objects.values('tokens', 'qtStopwordsTotal', 'qtAdverbiosTotal', 'qtTokenTotal').filter( name=nameDocument )
    
    if ( len(document) == 0 ):
        print('\n\tNenhum documento excluido, nome inexistente.')
        return False

    tokens = json.loads(document[0]['tokens'])

    allwords = json.loads(Global.objects.values('words').distinct()[0]['words'])
    qt_document = json.loads(Global.objects.values('qtDocument').distinct()[0]['qtDocument'])
    qt_stopwords = int( Global.objects.values('qtStopwords').distinct()[0]['qtStopwords'] ) - int( document[0]['qtStopwordsTotal'] )
    qt_adverbios = int( Global.objects.values('qtAdverbios').distinct()[0]['qtAdverbios'] ) - int( document[0]['qtAdverbiosTotal'] )
    qt_tokens = int( Global.objects.values('qtTokens').distinct()[0]['qtTokens'] ) - int( document[0]['qtTokenTotal'] )
    

    for key in tokens :
        if ( key in allwords ):
            allwords[key] -= tokens[key]
            if ( allwords[key] == 0 ):
                allwords.pop(key)
            
        if ( key in qt_document ):
            qt_document[key] -= 1
            if ( qt_document[key] == 0 ):
                qt_document.pop(key)
    
    print('\nallwords from global >>', allwords)
    Global(id=1, words=json.dumps(allwords, ensure_ascii=False),\
        qtStopwords=qt_stopwords, qtAdverbios=qt_adverbios, qtTokens=qt_tokens,\
        qtDocument=json.dumps(qt_document, ensure_ascii=False) ).save()
    return True

def update_global_insert( nameDocument = '' ):
    "Atualiza a frequencia global de palavras adicionado os tokens do documento a ser salvo"
    if (nameDocument == ''):
        print('\n\tNenhum documento salvo, nome do documento vazio.')
        return False

    document = Documents.objects.values('tokens', 'qtStopwordsTotal', 'qtAdverbiosTotal', 'qtTokenTotal').filter( name=nameDocument )
    
    if ( len(document) == 0 ):
        print('\n\tNenhum documento salvo, nome inexistente.')
        return False

    tokens = json.loads(document[0]['tokens'])

    allwords = json.loads(Global.objects.values('words').distinct()[0]['words'])
    qt_document = json.loads(Global.objects.values('qtDocument').distinct()[0]['qtDocument'])
    qt_stopwords = int( Global.objects.values('qtStopwords').distinct()[0]['qtStopwords'] ) + int( document[0]['qtStopwordsTotal'] )
    qt_adverbios = int( Global.objects.values('qtAdverbios').distinct()[0]['qtAdverbios'] ) + int( document[0]['qtAdverbiosTotal'] )
    qt_tokens = int( Global.objects.values('qtTokens').distinct()[0]['qtTokens'] ) + int( document[0]['qtTokenTotal'] )
    

    for key in tokens :
        if ( key in allwords ):
            allwords[key] += tokens[key]
        else:
            allwords[key] = tokens[key]
            
        if ( key in qt_document ):
            qt_document[key] += 1
        else:
            qt_document[key] = 1
    
    print('\nallwords from global >>', allwords)
    Global(id=1, words=json.dumps(allwords, ensure_ascii=False),\
        qtStopwords=qt_stopwords, qtAdverbios=qt_adverbios, qtTokens=qt_tokens,\
        qtDocument=json.dumps(qt_document, ensure_ascii=False) ).save()
    return True

def update_global_all():
    documents = Documents.objects.values('name').distinct()

    Global(id=1, words=json.dumps({}, ensure_ascii=False),\
        qtStopwords = 0, qtAdverbios = 0, qtTokens = 0,\
        qtDocument=json.dumps({}, ensure_ascii=False),\
        idf=json.dumps({}, ensure_ascii=False) ).save()
    for doc in documents:
        update_global_insert( doc['name'] )

    update_global_idf()
    return True
    
def remove_document( name ):
    pass

def insert_document( filename, texto ):
    # Get global word list
    words = json.loads(Global.objects.values('words').distinct()[0]['words'])

    # Calcula a frequencia de palavras no documento
    token = archive.get_frequency(archive.get_tokens(texto))
    print("TOKENS ",token)

    # Remove e conta as stopwords removidas
    token = archive.remove_stopwords( token )
    # Calcula a tf ajustada pelo tamanho do documento
    tf_adjusted = archive.get_tf( token['tokens'], token['qt_tok_total'] )
    tf_log = archive.get_tfLog( token['tokens'] )
    # Salva o novo documento no db
    Documents( name=filename, text=texto, tokens=json.dumps(token['tokens'], ensure_ascii=False),\
        tf=json.dumps( tf_adjusted, ensure_ascii=False),\
        tfLog=json.dumps( tf_log, ensure_ascii=False),\
        qtStopwords=token['qt_stopwords'], qtStopwordsTotal=token['qt_stopwords_total'],\
        qtAdverbios=token['qt_adverbios'], qtAdverbiosTotal=token['qt_adverbios_total'],\
        qtToken= token['qt_tok'], qtTokenTotal = token['qt_tok_total'], max=token['max'] ).save()

    # # Salva a frequencia global atualizada
    update_global_insert( filename )
    update_global_idf()
    # Global(id=1, words=json.dumps(words, ensure_ascii=False)).save()