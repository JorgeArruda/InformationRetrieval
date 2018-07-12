from django.shortcuts import render, render_to_response
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Documents
from .models import Global

import time
import os
import sys
import json
import math
# import numpy as np

import my_app.ri_vetorial.tokens.archive as archive
# from .mysql import update_global_all, update_global_idf, update_global_insert, update_global_remove, insert_document, remove_document
from .database import DB
# Create your views here.


def home(request):
    documents = Documents.objects.values('name').distinct()
    return render(request, 'my_app/documents.html', {'documents': documents})


@csrf_exempt
def upload_drive(request):
    # Get file
    upload_file = request.FILES['file']
    ret = []
    if upload_file:
        # Verifica se a pasta alvo já existe, se não, cria ela
        target_folder = settings.PULL_DRIVER_UPLOAD_PATH
        if not os.path.exists(target_folder):
            os.mkdir(target_folder)

        # Verifica se o arquivo já existe no bd
        filename = request.POST['filename']
        documents = Documents.objects.values('name').filter(name=filename)
        if (len(documents) != 0):
            return JsonResponse({"name": filename, "status": 'false'})

        # Save file in folder 'media'
        target = os.path.join(target_folder, filename)
        with open(target, 'wb+') as dest:
            for c in upload_file.chunks():
                dest.write(c)

        # Analisa o arquivo em busca de textos
        text = archive.get_text(filename, target_folder+'/')
        # Salva o novo documento no db
        DB().insert_document(filename, text)

        return JsonResponse({"name": filename, "status": 'true'})
    else:
        return HttpResponse(status=500)
    return HttpResponse(status=200)


@csrf_exempt
def getdocument(request):
    name = request.POST['name']
    document = Documents.objects.values('tokens', 'tf', 'tfLog', 'tfDouble').filter(name=name)
    if len(document) == 0:
        return render(request, 'my_app/show_document.html', {'words': {}})
    else:
        document = document[0]
        tokens = json.loads(document['tokens'])
        tf = json.loads(document['tf'])
        tfLog = json.loads(document['tfLog'])
        tfDouble = json.loads(document['tfDouble'])
        words = archive.sort_dic(tokens)
        line = []
        var = 1
        for word in words:
            line.append({'indice': var, 'word': word[0], 'frequency': word[1],
                         'tf': round(tf[word[0]], 2), 'tfLog': round(tfLog[word[0]], 2),
                         'tfDouble': round(tfDouble[word[0]], 2)})
            var += 1
        # for word in words:
        #     line.append({'indice': var, 'word': word[0], 'frequency': word[1],
        #                  'tf': iround(tf[word[0]]), 'tfLog': iround(tfLog[word[0]]),
        #                  'tfDouble': iround(tfDouble[word[0]])})
        #     var += 1
        # print(words)
        return render(request, 'my_app/show_document.html', {'words': line})


@csrf_exempt
def getglobal(request):
    name = request.POST['request']
    print('Get Global', name)
    values = Global.objects.values().distinct()[0]
    qtDocument = len(Documents.objects.values('name').distinct())
    list_documents = Documents.objects.values('name', 'qtStopwords', 'qtStopwordsTotal', 'qtAdverbios', 'qtAdverbiosTotal', 'qtToken', 'qtTokenTotal').distinct()
    qtWordsTotal = (values['qtTokens'] + values['qtStopwords'] + values['qtAdverbios'])

    documents_dict = []
    for item in list_documents:
        qtTokensTotal = item['qtTokenTotal']+item['qtStopwordsTotal']+item['qtAdverbiosTotal']
        if item['qtTokenTotal'] != 0:
            documents_dict.append(
                {'name': item['name'],
                 'qtWords': qtTokensTotal,
                 'qtStopwords': item['qtStopwordsTotal'],
                 'qtAdverbios': item['qtAdverbiosTotal'],
                 'qtTokens': item['qtTokenTotal'],
                 'qtWordsP': 100,
                 'qtStopwordsP': iround((item['qtStopwordsTotal']/qtTokensTotal)*100),
                 'qtAdverbiosP': iround((item['qtAdverbiosTotal']/qtTokensTotal)*100),
                 'qtTokensP': iround((item['qtTokenTotal']/qtTokensTotal)*100),
                 'qtDocument': qtDocument,
                 'documents': list_documents})
        else:
            documents_dict.append(
                {'name': item['name'],
                 'qtWords': item['qtTokenTotal'],
                 'qtStopwords': item['qtStopwordsTotal'],
                 'qtAdverbios': item['qtAdverbiosTotal'],
                 'qtTokens': qtTokens,
                 'qtWordsP': 100,
                 'qtStopwordsP': 0,
                 'qtAdverbiosP': 0,
                 'qtTokensP': 0,
                 'qtDocument': qtDocument,
                 'documents': list_documents})

    info = []
    if (qtDocument != 0):
        info.append(
            {'qtWords': qtWordsTotal,
             'qtStopwords': values['qtStopwords'],
             'qtAdverbios': values['qtAdverbios'],
             'qtTokens': values['qtTokens'],
             'qtWordsP': 100,
             'qtStopwordsP': iround((values['qtStopwords']/qtWordsTotal)*100),
             'qtAdverbiosP': iround((values['qtAdverbios']/qtWordsTotal)*100),
             'qtTokensP': iround((values['qtTokens']/qtWordsTotal)*100),
             'qtDocument': qtDocument,
             'documents': documents_dict})
    else:
        info.append({'qtWords': 0, 'qtStopwords': 0, 'qtAdverbios': 0,
                     'qtTokens': 0, 'qtWordsP': 0, 'qtStopwordsP': 0,
                     'qtAdverbiosP': 0, 'qtTokensP': 0, 'qtDocument': 0})

    # print('info', info)
    print(render(request, 'my_app/show_global.html', {'info': info}))
    return render(request, 'my_app/show_global.html', {'info': info})


@csrf_exempt
def getidf(request):
    print('Get IDF')
    name = request.POST['request']
    document = Global.objects.values('idf').distinct()[0]

    if len(document) == 0:
        return render(request, 'my_app/show_document.html', {'words': {}})
    else:
        idff = json.loads(document['idf'])
        words = sorted(idff)
        line = []
        var = 1
        for word in words:
            line.append({'indice': var, 'word': word, 'frequency': idff[word]})
            var += 1
        # print(words)
        return render(request, 'my_app/show_idf.html', {'words': line})


@csrf_exempt
def updateall(request):
    DB().update_global_all()
    documents = Documents.objects.values('name').distinct()
    return render(request, 'my_app/documents.html', {'documents': documents})


@csrf_exempt
def search(request):
    docs = []
    try:
        print('request.POST  ...  ', request.POST)
        query = request.POST['text']
        strategyTF = request.POST['tfType']
        strategyIDF = request.POST['idfType']
        print('Query: ', query)
        docs = DB().search(query, strategyTF, strategyIDF)
        for doc in docs:
            print('Name: ', doc['name'])
    except MultiValueDictKeyError:
        print('Error search() in views.py line 189')
    return render(request, 'my_app/search.html', {'list_doc': docs})


@csrf_exempt
def busca(request):
    docs = []
    try:
        query = request.POST['text']
        strategyTF = request.POST['tfType']
        strategyIDF = request.POST['idfType']
        print('request.POST: ', request.POST)
        docs = DB().search(query, strategyTF, strategyIDF)
        for doc in docs:
            print('Name: ', doc['name'])
    except MultiValueDictKeyError:
        print('Error search() in views.py line 203')
    return render(request, 'search.html', {'list_doc': docs})


def documents(request):
    return render(request, 'my_app/documents.html', {'title': 'Documentos'})


def teste(request):
    return render(request, 'index.html', {'title': 'Documentos'})


def roundd(val, digits):
    return round(val+10**(-len(str(val))-1), digits)


def iround(x):
    """iround(number) -> integer
    Round a number to the nearest integer."""
    y = round(x) - .5
    return int(y) + (y > 0)
