from django.urls import path
from . import views
urlpatterns = [
    path('databank/login/', views.login_page, name="login-page"),
    path('logout/', views.logout_user, name='logout-page'),
]
