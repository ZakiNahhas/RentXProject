from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from .models import *
import bcrypt

def cover(request):

    return render(request, "cover.html")

def login_page(request):

    return render(request, "login.html")

def register_page(request):

    return render(request, "registration.html")

# def index(request):
#     return render(request, "cover.html")


def adminreport(request):

    context={
            'freeproducts':Product.objects.filter(price=0),
            'rents': Rental.objects.all(),
            'lowproducts':Product.objects.order_by("price"),
            'products':Product.objects.all(),
            'users':User.objects.all(),
            'rentedproducts':Product.objects.filter(status=1),
            'availableproducts':Product.objects.filter(status=0),

            'rented':Rental.objects.annotate(product_count=Count('rented_product')).order_by('-rented_product'),
            'likeproducts':Product.objects.annotate(like_count=Count('liked_by')).order_by('-liked_by'),
            'freeproductsno':Product.objects.filter(price=0).annotate(Count("name")),
            'activerentsno':Product.objects.filter(status=1).annotate(Count("name")),
            'availableproductsnum':Product.objects.filter(status=0).annotate(Count("name")),
            'userno':User.objects.annotate(Count("id")),
            'rentersno':Product.objects.values("offered_by").annotate(Count("id"))
        }
    return render(request, 'adminreport.html',context)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_page')
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

        return redirect('/login_page')

    user = existing_user[0]

    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Please enter valid credentials.")

        return redirect('/login_page')

    request.session['firstname'] = user.firstname
    request.session['lastname'] = user.lastname
    request.session["userid"] = user.id
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
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



def searching(request):
    request.session['search'] =request.POST['search']
    search_in= request.session['search']
    context={
        "user": User.objects.get(id=request.session["userid"]),
        'products':Product.objects.filter(name__contains=search_in).all(),
    }
   
    return render(request, 'out.html', context)



def filtering(request):
    if request.POST['filterproducts']=='free':
        context={
           
            'freeproducts':Product.objects.filter(name__contains=request.session['search'],price=0).all()
        }

    if request.POST['filterproducts']=='low':
        context={
            'lowproducts':Product.objects.filter(name__contains=request.session['search']).order_by("price")
        }

    if request.POST['filterproducts']=='like':
        context={
            'likeproducts':Product.objects.filter(name__contains=request.session['search']).annotate(like_count=Count('liked_by')).order_by('-liked_by')
        }
    return render(request, 'free.html',context)


def my_profile(request):
    context={
        'user': User.objects.get(id=request.session['userid'])
    }
    return render(request, 'profile.html', context)

# def categories(request):
#     return render(request, 'categories.html')

def add_a_product(request):
    context={
        'categories': Category.objects.all(),
        'products': Product.objects.all()
    }
    
    return render(request, 'add_a_product.html',context)


def create(request):
     errors = Product.objects.basic_validator(request.POST)
     if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/add_a_product')
     else:
        userx= User.objects.get(id=request.session['userid'])
        category= Category.objects.get(id=request.POST['selectcategory'])
        pimage=request.FILES['proimage']
        
        Product.objects.create(name=request.POST['name'], offered_by=userx, description=request.POST['desc'],  price=request.POST['price'],location=request.POST['location'], category=category,product_image=pimage)
        

        return redirect('/my_profile')

def delete_product(request,id):
    deleted_product= Product.objects.get(id=int(id))
    deleted_product.delete()

    
    return redirect('/my_profile')

def oneproduct(request,id):
    context={
        'oneproduct': Product.objects.get(id=int(id)),
        'user':User.objects.get(id=request.session['userid'])
    }
    return render(request, 'product.html', context)

def editproduct(request,id):
    context={
        "oneproduct" : Product.objects.get(id=id),
        'categories': Category.objects.all
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
        category= Category.objects.get(id=request.POST['selectcategory'])
        productinstance.category=category
        productinstance.product_image=request.FILES['proimage']
        productinstance.save()
           
        
        return redirect("/my_profile")

def officecat(request):
    
    context={
       
        'products': Product.objects.all()

    }
    return render(request, 'office.html', context)

def electcat(request):
    context={
       
        'products': Product.objects.all()
    
    }

    return render(request, 'elect.html', context)

def homecat(request):
    
    context={
       
        'products': Product.objects.all()

    }
    return render(request, 'home.html', context)

def filtering(request):
    if request.POST['filterproducts']=='free':
        context={
           
            'freeproducts':Product.objects.filter(name__contains=request.session['search'],price=0).all()
        }

    if request.POST['filterproducts']=='low':
        context={
            'lowproducts':Product.objects.filter(name__contains=request.session['search']).order_by("price")
        }

    if request.POST['filterproducts']=='like':
        context={
            'likeproducts':Product.objects.filter(name__contains=request.session['search']).annotate(like_count=Count('liked_by')).order_by('-liked_by')
        }
    return render(request, 'free.html',context)








def addtowish(request,id):
    userliking= User.objects.get(id=request.session['userid'])
    likedproduct=Product.objects.get(id=int(id))
    likedproduct.liked_by.add(userliking)
    likedproduct.save()
    return redirect('/show/'+str(id))

def unwish(request,id):
    userunlike= User.objects.get(id=request.session['userid'])
    unlikedproduct=Product.objects.get(id=int(id))
    unlikedproduct.liked_by.remove(userunlike)
    unlikedproduct.save()
    return redirect('/show/'+str(id))


def renting(request,id):
    product_x= Product.objects.get(id=int(id))
    product_x.status=1
    product_x.save()
    userof= product_x.offered_by.id
    renter= User.objects.get(id=userof)
    
    Rental.objects.create(renter=renter,rented_product=product_x)
    theuser=  User.objects.get(id=request.session['userid'])
    rent_x= Rental.objects.last()
    rent_x.rentee.add(theuser)
    rent_x.save()
    return redirect("/my_profile")




# def rentdone(request,id):
#     context={
#         'rentedproduct':Product.objects.get(id=int(id)),
#         'rentee': User.objects.get(id=request.session['userid']),
#         'rents': Rental.objects.filter(rented_product=Product.objects.get(id=int(id)))
#     }
#     return render(request, 'form.html', context)

def unrent(request,id):
    rentee= User.objects.get(id=request.session['userid'])
    order_x= Rental.objects.get(id=int(id))
    product_x=order_x.rented_product
    product_x.status = 0
    product_x.save()
    order_x.rentee.remove(rentee)
    order_x.save()
    
    return redirect("/my_profile")

























def adminform(request):
    
    return render(request, 'adminform.html')

def admincreate(request):
    
    Category.objects.create(name=request.POST['name'])
    return redirect("/adminz/dash")




def admindash(request):
    context={
        'categories': Category.objects.all
    }
    
    return render(request, 'admindash.html',context)


def delete_category(request,id):
    deleted_category= Category.objects.get(id=int(id))
    deleted_category.delete()

    
    return redirect("/adminz/dash")











def offer(request):
    context={
        'categories': Category.objects.all
    }
    return render(request, 'newitem.html',context)





def show(request):
    context={
        'products': Product.objects.all()
    }
    return render(request, 'show.html', context)