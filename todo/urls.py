from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup, name="signup"),
    path("login/", views.loginn, name="login"),
    path("todopage/", views.todo, name="todo"),
]
