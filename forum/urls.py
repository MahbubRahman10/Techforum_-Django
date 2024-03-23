from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Home-Page'),
    path('view/<int:pk>/', views.viewquestion, name='Viewquestion-Page'),
    path('reply/<int:pk>/', views.replyquestion, name='Reply-Question'),
    path('reply/update/<int:pk>/', views.updatereply, name='Update-Reply'),
    path('reply/delete/<int:pk>/', views.deletereply, name='Delete-Reply'),
    path('reply/best/<int:pk>/', views.bestreply, name='Best-Reply'),
    path('reply/like', views.likereply, name='Like-Reply'),
    path('category/<int:pk>/', views.category, name='Category-Page'),
    path('question', views.addquestion, name='Add Question Page'),
    path('question/edit/<int:pk>/', views.editquestion, name='Edit Question Page'),
]
