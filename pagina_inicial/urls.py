from django.urls import path
from .views import *

app_name = 'pagina_inicial'
urlpatterns = [
    path('', home, name = 'home')
]