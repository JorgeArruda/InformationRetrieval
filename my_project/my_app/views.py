from django.shortcuts import render
from .models import Documents
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time
import os
import json

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
        rtime = str( int( time.time() ) )
        filename = request.POST['filename']
        target = os.path.join(target_folder, filename)
        with open(target, 'wb+') as dest:
            for c in upload_file.chunks():
                dest.write(c)
        # ret['file_remote_path'] = target
    else:
        return HttpResponse(status=500)
    return HttpResponse()