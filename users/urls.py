from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, ProfileUpdateView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('register/', RegisterView.as_view()),
    path('profile/<int:pk>/', ProfileUpdateView.as_view()),
]