from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('previews/', views.getMessagePreviews, name='previews')
    path('csrf/', views.csrf),
]