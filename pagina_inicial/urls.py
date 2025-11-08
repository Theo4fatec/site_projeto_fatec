from django.urls import path
from .views import *

app_name = 'pagina_inicial'
urlpatterns = [
    path('', home, name = 'home'),
    path('accounts/login/', login_cadastro, name = 'login_cadastro'),
    path('accounts/logout/', logout_usuario, name = 'logout_usuario'),
    path('cadastro', cadastro_usuario, name = 'cadastro_usuario'),
]