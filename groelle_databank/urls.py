from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static  # for images
from django.conf import settings  # for images
# from django.views.generic.base import RedirectView  # class-based view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("databank.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
