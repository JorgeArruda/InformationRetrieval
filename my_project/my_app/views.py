from django.shortcuts import render
from uploads.core.models import Document
# Create your views here.

def home(request):
    documents = Document.objects.all()
    return render(request, 'core/home.html', { 'documents': documents })
