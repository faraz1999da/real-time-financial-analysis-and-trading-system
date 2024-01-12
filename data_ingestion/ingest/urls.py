from django.urls import path
from .views import ingest
app_name = 'ingest'
urlpatterns = [
    path('', ingest, name='ingest-data'),
]