from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Documents
from .models import Global

import time
import os
import sys
import json
import math
import numpy as np

import my_app.ri_vetorial.archive as archive
import my_app.mysql as mysql

# Create your views here.

def home(request):
    documents = Documents.objects.values('name').distinct()
    return render(request, 'my_app/home.html', { 'documents': documents })

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
        if ( len(documents) != 0 ):
            return JsonResponse({"name": filename, "status": 'false'})

        # Save file in folder 'media'
        target = os.path.join(target_folder, filename)
        with open(target, 'wb+') as dest:
            for c in upload_file.chunks():
                dest.write(c)

        # Analisa o arquivo em busca de textos
        text = archive.get_text(filename, target_folder+'/')
        # Salva o novo documento no db
        mysql.insert_document( filename, text )

        return JsonResponse({"name": filename, "status": 'true'})
    else:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

@csrf_exempt
def getdocument(request):
    name = request.POST['name']
    document = Documents.objects.values('tokens', 'tf', 'tfLog', 'tfDouble').filter(name=name)
    if len(document) == 0:
        return render(request, 'my_app/show_document.html', { 'words': {} })
    else:
        document = document[0]
        tokens = json.loads( document['tokens'] )
        tf = json.loads( document['tf'] )
        tfLog = json.loads( document['tfLog'] )
        tfDouble = json.loads( document['tfDouble'] )
        words = archive.sort_dic( tokens )
        line = []
        var = 1
        for word in words:
            line.append({'indice':var, 'word':word[0], 'frequency': word[1], 'tf': round(tf[word[0]], 2), 'tfLog': round(tfLog[word[0]], 2), 'tfDouble': round(tfDouble[word[0]], 2) } )
            var+=1
        # print(words)
        return render(request, 'my_app/show_document.html', { 'words': line })
# tf = mode
# tfLog = m
# tfDouble 

@csrf_exempt
def getglobal(request):
    name = request.POST['request']
    print('Get Global', name)
    values = Global.objects.values().distinct()[0]
    qtDocument = len(Documents.objects.values('name').distinct())
    qtWords = ( values['qtTokens'] - values['qtStopwords'] - values['qtAdverbios'] )
    info = []
    info.append({ 'qtWords': values['qtTokens'],\
        'qtStopwords': values['qtStopwords'],\
        'qtAdverbios': values['qtAdverbios'],\
        'qtTokens': qtWords,\
        'qtWordsP': 100,\
        'qtStopwordsP': iround( (values['qtStopwords']/values['qtTokens'])*100),\
        'qtAdverbiosP': iround( (values['qtAdverbios']/values['qtTokens'])*100),\
        'qtTokensP': iround( (qtWords/values['qtTokens'])*100),\
        'qtDocument': qtDocument })

    # tokens = Documents.objects.values('tokens').filter(name=name)
    # if len(tokens) == 0:
    #     return render(request, 'my_app/show_document.html', { 'words': {} })
    # else:
    #     tokens = json.loads(tokens[0]['tokens'])
    #     words = []
    #     var = 1
    #     for word in tokens:
    #         words.append({'indice':var, 'word':word, 'frequency': tokens[word]})
    #         var+=1
    #     # print(words)
    print('info', info)
    print(render(request, 'my_app/show_global.html', { 'info': info }))
    return render(request, 'my_app/show_global.html', { 'info': info })


def roundd(val,digits):
   return round(val+10**(-len(str(val))-1), digits)

def iround(x):
    """iround(number) -> integer
    Round a number to the nearest integer."""
    y = round(x) - .5
    return int(y) + (y > 0)