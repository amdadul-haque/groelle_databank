from django.urls import path
from . import views
urlpatterns = [
    path('databank/', views.databank_page, name="databank-page"),
    path('databank/filter/<slug:slug>/', views.artistworks_page, name="artistworks-page"),
    path('databank/edit/<slug:slug>/', views.editwork_page, name="editwork-page"),
    path('databank/sale/<slug:slug>/', views.salework_page, name="salework-page"),
    path('databank/wuppertal/', views.wuppertal_page, name="wuppertal-page"),
    path('databank/duesseldorf/', views.duesseldorf_page, name="duesseldorf-page"),
    path('databank/add/add-work/', views.addwork_page, name="addwork-page"),
    path('databank/add/add-artist/', views.addartist_page, name="addartist-page"),
    path('databank/create/pricelist-creation/', views.create_pricelist, name="create-pricelist"),
    path('databank/create/invoice-creation/',
         views.create_invoice, name="create-invoice"),
#     path('databank/slider/<slug:slug>',
#          views.artist_slide_page, name="artist-slide-page"),
]
