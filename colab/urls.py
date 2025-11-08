from django.urls import path
from .views import *

app_name = 'colab'
urlpatterns = [
    path('teste', teste, name = 'teste'),
    path('grafico_banco', grafico_banco, name = 'grafico_banco')

]