from django.urls import path
from . import views


urlpatterns = [
    path("databank/rest-api/art-list", views.getArtworkList, name="art-list"),
    path("databank/rest-api/art-details/<int:pk>", views.getArtworkDetails, name="art-details"),
    path("databank/rest-api/art-details/download/<int:pk>",
         views.downloadArtworkDetails, name="art-details-download")
]
