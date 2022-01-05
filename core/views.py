from django.shortcuts import render
from django.contrib.auth import authenticate, login

# import user
from django.contrib.auth.models import User

# import httpresponse
from django.http import HttpResponse

# Create your views here.


def index(request):
    # return render(request, 'this is index')
    return render(request, "index.html", {})


def loginView(request):

    uname = request.POST.get("username")
    pas = request.POST.get("password")
    print(uname)
    print(pas)
    user = authenticate(request, username=uname, password=pas)

    if User is not None:
        login(request, user)
    else:
        pass

    return render(request, "home.html", {})
