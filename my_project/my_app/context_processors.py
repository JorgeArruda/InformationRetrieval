# encoding=utf-8

from .models import Documents


def documents_name(request):
    return {
        'documents_name': Documents.objects.values('name').distinct()
    }
