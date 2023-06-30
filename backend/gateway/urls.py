from django.urls import path
from .views import LoginView, Registerview

urlpatterns = [
    path('sign-in/', LoginView.as_view()),
    path('sign-up/', Registerview.as_view()),
]