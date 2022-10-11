from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.success_page),
    path('my_profile', views.my_profile),
    path('office', views.categories),
    path('add_a_product', views.add_a_product),
    path('create', views.create),
    path('show', views.show),
    path('del/<int:id>', views.delproduct),
    path('edit/<int:id>', views.editproduct),
    path('update/<int:id>', views.updateproduct),
    path('adminz/form', views.adminform),
    path('adminz/create', views.admincreate),
    path('adminz/dash', views.admindash),
    path("cat/del/<int:id>", views.delcat),
]