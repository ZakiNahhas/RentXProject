from django.urls import path

from . import views

urlpatterns = [
    path('', views.cover),
    path('register', views.register),
    path('register_page', views.register_page),
    path('login_page', views.login_page),
    
    # path('cover', views.index),
    # path('register', views.register),
    path('login', views.login),
    path('logout/', views.logout),
    path('dashboard', views.success_page),
    path('my_profile', views.my_profile),
    # path('office', views.categories),
    path('add_a_product', views.add_a_product),
    path('create', views.create),
    # path('show', views.show),
    path("show/<int:id>", views.oneproduct),
    path('delete/<int:id>', views.delete_product),
    # path('edit/<int:id>', views.editproduct),
    # path('update/<int:id>', views.updateproduct),
    path('adminz/form', views.adminform),
    path('adminz/create', views.admincreate),
    path('adminz/dash', views.admindash),
    # path("cat/del/<int:id>", views.delcat),
]