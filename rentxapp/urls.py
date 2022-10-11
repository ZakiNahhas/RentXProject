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
    path('add_a_product', views.add_a_product)
]