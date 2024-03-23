from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('blog', views.index, name='Blog-Page'),
    path('blog/view/<int:pk>/', views.viewpost, name='Viewpost-Page'),
    path('blog/comment/<int:pk>/', views.blogcomment, name='Blogcomment-Page'),
]
