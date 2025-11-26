from django.urls import path
from .views import *

app_name = 'colab'
urlpatterns = [
    path('teste', teste, name = 'teste'),
    path('grafico_banco', grafico_banco, name = 'grafico_banco'),
    path('grafico_1', grafico_1, name="grafico_1"),
    path('powerbi', powerbi, name='powerbi'),
    path('powerbi_2', powerbi_2, name='powerbi_2'),
    path('powerbi_3', powerbi_3, name='powerbi_3'),
    path('powerbi_4', powerbi_4, name='powerbi_4'),

]
