from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('previews/', views.getMessagePreviews, name='previews'),
    path('conversation/', views.getMessagesBetween, name='conversation'),
    path('search/', views.searchForUser, name='search'),
    path('id/', views.getMyId, name='id'),
    path('csrf/', views.csrf),
]