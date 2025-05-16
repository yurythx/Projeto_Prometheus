"""
URLs para a raiz da API
"""

from django.urls import path
from .views import api_root

urlpatterns = [
    path('', api_root, name='api-root'),
]
