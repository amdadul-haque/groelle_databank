from django.urls import path
from . import views
urlpatterns = [
    path('databank/', views.databank_page, name="databank-page"),
    path('databank/<str:pk>', views.artistworks_page, name="artistworks-page")
]
