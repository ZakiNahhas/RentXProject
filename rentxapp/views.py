from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "registration.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()  
        user = User.objects.create(
        firstname=request.POST["firstname"],
        lastname=request.POST["lastname"],
        email=request.POST["email"],
        password=pw_hash
    )
        user=User.objects.last()
        request.session['firstname'] = user.firstname
        request.session["userid"] = user.id
    return redirect('/dashboard')

def login(request):
    existing_user = User.objects.filter(email=request.POST['email'])

    if len(existing_user) == 0:
        messages.error(request, "Please enter valid credentials.")

        return redirect('/')

    user = existing_user[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please enter valid credentials.")

        return redirect('/')

    request.session['firstname'] = user.firstname
    request.session['lastname'] = user.lastname
    request.session["userid"] = user.id
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    # request.session.pop("user_id")
    return redirect('/')

def success_page(request):
    if "userid" not in request.session:
        messages.error(request, "You must log in to view this page!")
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session["userid"]),
        'products': Product.objects.all()
    }
    return render(request, "dashboard.html", context)
def my_profile(request):
    return render(request, 'profile.html')

def categories(request):
    return render(request, 'categories.html')

def add_a_product(request):
    
    return render(request, 'add_a_product.html')