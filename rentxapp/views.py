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
    context={
        'theuser': User.objects.get(id=request.session['userid'])
    }
    return render(request, 'profile.html', context)

def categories(request):
    return render(request, 'categories.html')

def add_a_product(request):
    context={
        'cats': Category.objects.all
    }
    
    return render(request, 'add_a_product.html',context)


def oneproduct(request,id):
    context={
        'oneproduct': Product.objects.get(id=int(id))
    }
    return render(request, 'product.html', context)

def delproduct(request,id):
    deleted_product= Product.objects.get(id=int(id))
    deleted_product.delete()

    
    return redirect('/my_profile')

def editproduct(request,id):
    context={
        "oneproduct" : Product.objects.get(id=id),
        'cats': Category.objects.all

    }
    
    return render(request, 'edit.html', context)



def updateproduct(request,id):
    
    errors = Product.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit/'+str(id))
    else:

        productinstance = Product.objects.get(id=id)
        
        productinstance.name=request.POST["name"]
        productinstance.price=request.POST["price"]
        productinstance.location=request.POST["location"]
        productinstance.description=request.POST["desc"]
        category_z= Category.objects.get(id=request.POST['selectcategory'])
        productinstance.category=category_z
        productinstance.save()
           
        
        return redirect("/my_profile")



def renting(request,id):
    product_x= Product.objects.get(id=int(id))
    userof= product_x.offered_by.id
    renter= User.objects.get(id=userof)
    rentee=  User.objects.get(id=request.session['userid'])
    Rental.objects.create(renter=renter,rentee=rentee,rented_product=product_x, status=0)
    return redirect('/rentdone/'+str(id))

def rentdone(request,id):
    rentedproduct=Product.objects.get(id=int(id))
    rent_of_this_product = rentedproduct

    context={
        'rentedproduct':Product.objects.get(id=int(id)),
        'ordertaker': User.objects.get(id=request.session['userid']),
        'rents': Rental.objects.all()
    }
    return render(request, 'form.html', context)

def adminform(request):
    
    return render(request, 'adminform.html')

def admincreate(request):
    
    Category.objects.create(name=request.POST['name'])
    return redirect("/adminz/dash")

def admindash(request):
    context={
        'cats': Category.objects.all
    }
    
    return render(request, 'admindash.html',context)


def delcat(request,id):
    deleted_cat= Category.objects.get(id=int(id))
    deleted_cat.delete()

    
    return redirect("/adminz/dash")

def offer(request):
    context={
        'cats': Category.objects.all
    }
    return render(request, 'newitem.html',context)


def create(request):
     errors = Product.objects.basic_validator(request.POST)
     if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/add_a_product')
     else:
        userx= User.objects.get(id=request.session['userid'])
        category_x= Category.objects.get(id=request.POST['selectcategory'])
        
        Product.objects.create(name=request.POST['name'], offered_by=userx, description=request.POST['desc'],  price=request.POST['price'],location=request.POST['location'], category=category_x)
        

        return redirect('/show')


def show(request):
    context={
        'products': Product.objects.all()
    }
    return render(request, 'show.html', context)