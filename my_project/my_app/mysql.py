#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .models import Documents
from .models import Global

import json
import math

import my_app.ri_vetorial.archive as archive

def update_global_idf():
    "Atualiza o idf global"

    qt_document = json.loads(Global.objects.values('qtdocument').distinct()[0]['qtdocument'])
    gl = Global.objects.values().distinct()[0]
    idf_word = {}
    for key in qt_document :
        qt_total = len(Documents.objects.values('nome').distinct())
        idf_word[key] = math.log( qt_total / qt_document[key], 2 )

    gl['idf'] = json.dumps(idf_word, ensure_ascii=False)
    Global(id=1, words=gl['words'],\
        qtstopwords=gl['qtstopwords'], qtadverbios=gl['qtadverbios'], qttokens=gl['qttokens'],\
        qtdocument=gl['qtdocument'],\
        idf=gl['idf'] ).save()
    return True

def update_tf_normalized( nameDocument ):
    id_doc = Documents.objects.values('id', 'tokens').filter( nome=nameDocument )
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
        
    document = Documents.objects.values('tokens', 'qtstopwordstotal', 'qtadverbiostotal', 'qttoktotal').filter( nome=nameDocument )
    
    if ( len(document) == 0 ):
        print('\n\tNenhum documento excluido, nome inexistente.')
        return False

    tokens = json.loads(document[0]['tokens'])

    allwords = json.loads(Global.objects.values('words').distinct()[0]['words'])
    qt_document = json.loads(Global.objects.values('qtdocument').distinct()[0]['qtdocument'])
    qt_stopwords = int( Global.objects.values('qtstopwords').distinct()[0]['qtstopwords'] ) - int( document[0]['qtstopwordstotal'] )
    qt_adverbios = int( Global.objects.values('qtadverbios').distinct()[0]['qtadverbios'] ) - int( document[0]['qtadverbiostotal'] )
    qt_tokens = int( Global.objects.values('qttokens').distinct()[0]['qttokens'] ) - int( document[0]['qttoktotal'] )
    

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
        qtstopwords=qt_stopwords, qtadverbios=qt_adverbios, qttokens=qt_tokens,\
        qtdocument=json.dumps(qt_document, ensure_ascii=False) ).save()
    return True

def update_global_insert( nameDocument = '' ):
    "Atualiza a frequencia global de palavras adicionado os tokens do documento a ser salvo"
    if (nameDocument == ''):
        print('\n\tNenhum documento salvo, nome do documento vazio.')
        return False

    document = Documents.objects.values('tokens', 'qtstopwordstotal', 'qtadverbiostotal', 'qttoktotal').filter( nome=nameDocument )
    
    if ( len(document) == 0 ):
        print('\n\tNenhum documento salvo, nome inexistente.')
        return False

    tokens = json.loads(document[0]['tokens'])

    allwords = json.loads(Global.objects.values('words').distinct()[0]['words'])
    qt_document = json.loads(Global.objects.values('qtdocument').distinct()[0]['qtdocument'])
    qt_stopwords = int( Global.objects.values('qtstopwords').distinct()[0]['qtstopwords'] ) + int( document[0]['qtstopwordstotal'] )
    qt_adverbios = int( Global.objects.values('qtadverbios').distinct()[0]['qtadverbios'] ) + int( document[0]['qtadverbiostotal'] )
    qt_tokens = int( Global.objects.values('qttokens').distinct()[0]['qttokens'] ) + int( document[0]['qttoktotal'] )
    

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
        qtstopwords=qt_stopwords, qtadverbios=qt_adverbios, qttokens=qt_tokens,\
        qtdocument=json.dumps(qt_document, ensure_ascii=False) ).save()
    return True

def update_global_all():
    documents = Documents.objects.values('nome').distinct()

    Global(id=1, words=json.dumps({}, ensure_ascii=False),\
        qtstopwords = 0, qtadverbios = 0, qttokens = 0,\
        qtdocument=json.dumps({}, ensure_ascii=False),\
        idf=json.dumps({}, ensure_ascii=False) ).save()
    for doc in documents:
        update_global_insert( doc['nome'] )

    update_global_idf()
    return True
    
def remove_document( name ):
    pass

def insert_document( filename, text ):
    # Get global word list
    words = json.loads(Global.objects.values('words').distinct()[0]['words'])

    # Calcula a frequencia de palavras no documento
    tokens = archive.get_frequency(archive.get_tokens(text))
    print("TOKENS ",tokens)

    # Remove e conta as stopwords removidas
    tokens = archive.remove_stopwords( tokens )

    # Salva o novo documento no db
    Documents(nome=filename, texto=text, tokens=json.dumps(tokens['tokens'], ensure_ascii=False),\
        qtstopwords=tokens['qt_stopwords'], qtstopwordstotal=tokens['qt_stopwords_total'],\
        qtadverbios=tokens['qt_adverbios'], qtadverbiostotal=tokens['qt_adverbios_total'],\
        qttok = tokens['qt_tok'], qttoktotal = tokens['qt_tok_total'], max=tokens['max'] ).save()

    # # Salva a frequencia global atualizada
    update_global_insert( filename )
    update_global_idf()
    # Global(id=1, words=json.dumps(words, ensure_ascii=False)).save()