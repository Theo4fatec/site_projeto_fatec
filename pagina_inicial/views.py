from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    return render(request, 'pagina_inicial/home.html')

def login_cadastro(request):
    if request.method == "GET":
        return render(request, 'pagina_inicial/login_cadastro.html', { "next": request.GET.get("next") })
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        next = request.POST.get("next")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if next and next != "None":
                return redirect(next)
            else:
                return redirect("/")
        else:
            return render(request, 'pagina_inicial/login_cadastro.html')

def logout_usuario(request):
    logout(request)
    return redirect("/")


def cadastro_usuario(request):
	if request.method == "GET":
		return render(request, "pagina_inicial/cadastro_usuario.html")
	else:
		post = request.POST
		user = User.objects.create_user(
			username = post.get("username"),
			email = post.get("email"),
			first_name = post.get("first_name"),
			last_name = post.get("last_name"),
			password = post.get("password")
		)
		user = authenticate(
			username=post.get("username"),
			password=post.get("password")
		)
		login(request, user)
		return redirect("/")