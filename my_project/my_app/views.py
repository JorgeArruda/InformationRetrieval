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

import my_app.ri_vetorial.archive as archive

# Create your views here.

def home(request):
    documents = Documents.objects.values('nome').distinct()
    return render(request, 'my_app/home.html', { 'documents': documents })

@csrf_exempt
def upload_drive(request):
    upload_file = request.FILES['file']
    ret = []
    if upload_file:
        target_folder = settings.PULL_DRIVER_UPLOAD_PATH

        if not os.path.exists(target_folder):
            os.mkdir(target_folder)
        documents = Documents.objects.values('nome').distinct()
        filename = request.POST['filename']
        if (documents):
            for document in documents:
                if ( str(document['nome']) ==  str(filename)):
                    return JsonResponse({"nome": filename, "status": 'false'})

        target = os.path.join(target_folder, filename)
        with open(target, 'wb+') as dest:
            for c in upload_file.chunks():
                dest.write(c)
        words = json.loads(Global.objects.values('words').distinct()[0]['words'])

        text = archive.get_text(filename, target_folder+'/')
        (tokens, words) = archive.get_frequency(archive.get_tokens(text), words)
        print("TOKENS ",tokens)
        Documents(nome=filename, texto=text, tokens=json.dumps(tokens, ensure_ascii=False)).save()
        Global(id=1, words=json.dumps(words, ensure_ascii=False)).save()

        return JsonResponse({"nome": filename, "status": 'true'})
    else:
        return HttpResponse(status=500)
    return HttpResponse(status=200)

@csrf_exempt
def getdocument(request):
    name = request.POST['name']
    tokens = json.loads(Documents.objects.values('tokens').filter(nome=name)[0]['tokens'])
    words = []
    var = 1
    for word in tokens:
        words.append({'indice':var, 'word':word, 'frequency': tokens[word]})
        var+=1
    print(words)
    return render(request, 'my_app/show_document.html', { 'words': words })