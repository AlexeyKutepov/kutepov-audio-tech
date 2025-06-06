"""KAT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.contacts, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<id>/', views.unsubscribe, name='unsubscribe'),
    path('blog/<url>/', views.post, name='post'),
    path('blog/', views.blog, name='blog'),
    path('products/<url>/', views.product_details, name='product_details'),
    path('products/', views.products, name='products'),
]
