from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from todo import models


# Create your views here.
def signup(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        print(fnm, email, pwd)

        try:
            my_user = User.objects.create_user(username=fnm, email=email, password=pwd)
            my_user.save()
            return redirect('/login')
        except IntegrityError:
            return render(request, "signup.html", {'error': 'Username already exists. Please choose another one.'})

    return render(request, "signup.html")


def loginn(request):
    if request.method == "POST":
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        print(fnm,pwd)
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/todopage')
        else:
            return redirect('/login')

    return render(request, "login.html")

@login_required(login_url='/login')
def todo(request):
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)  # Debugging print statement

        obj = models.TODOO(title=title, user=request.user)
        obj.save()

        # Correct ordering field, assuming it's 'date'
        res = models.TODOO.objects.filter(user=request.user).order_by('-date')
        return redirect('/todopage')

    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, "todo.html", {'res': res})


@login_required(login_url='/login')
def edit_todo(request, srno):
    if request.method == "POST":
        title = request.POST.get('title')
        print(title)  # Debugging print statement

        obj = models.TODOO.objects.get(srno=srno)
        obj.title=title
        obj.save()
        user = request.user

        # Correct ordering field
        return redirect('/todopage' )

    obj = models.TODOO.objects.get(srno=srno)
    return render(request, "edit_todo.html",{'obj':obj})

@login_required(login_url='/login')
def delete_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login')