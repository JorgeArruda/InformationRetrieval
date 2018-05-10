from django.shortcuts import render
from .models import Documents
# Create your views here.

def home(request):
    documents = Documents.objects.all()
    return render(request, 'my_app/home.html', { 'documents': documents })
