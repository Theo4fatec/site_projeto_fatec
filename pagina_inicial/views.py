from django.shortcuts import render

def home(request):
    return render(request, 'pagina_inicial/home.html')