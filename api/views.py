# this will take any python or serialized data and render it as json data
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from databank.models import Work
from .serializers import WorkSerializer
import urllib.request


@api_view(["GET"])
def getArtworkList(request):
    works = Work.objects.all()
    serializer = WorkSerializer(works, many=True)
    return Response(serializer.data)



@api_view(["GET"])   
def getArtworkDetails(request, pk):
    work = Work.objects.get(pk=pk)
    serializer = WorkSerializer(work)
    return Response(serializer.data)



@api_view(["GET"])
def downloadArtworkDetails(request, pk):
    work = get_object_or_404(Work, pk=pk)
    serializer = WorkSerializer(work)
    work_details = serializer.data
    image_url = 'http://' + request.get_host() + work_details["image_url"]
    
    title = work_details["name"]
    materials = work_details["materials"]
    date = str(work_details["production_date"])
    width = str(work_details["width"])
    height = str(work_details["height"])
    price = str(work_details["price"])
    
    image_name = "_".join(
        [title, date, materials, width, height, price])
    
    urllib.request.urlretrieve(image_url, image_name)  # Download image
    with open(image_name, 'rb') as f:
        response = HttpResponse(f.read(), content_type="image/jpeg")
        response['Content-Disposition'] = f'attachment; filename="{image_name}"'
        return response
