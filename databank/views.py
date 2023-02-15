from django.shortcuts import render, redirect
from .models import Work, Artist, Status
from .forms import StatusForm, WorkForm

# Create your views here.


def databank_page(request):
    artists = Artist.objects.all()
    works = Work.objects.all()

    content = {"artists": artists,
               "works": works,
               }
    return render(request, "databank/index.html", content)


def artistworks_page(request, pk):
    artists = Artist.objects.all()
    artist = Artist.objects.get(pk=pk)
    works = Work.objects.filter(artist__id=pk)
    statusform = StatusForm()
    

    if request.method == "POST":
        statusform = StatusForm(request.POST)
        if statusform.is_valid():
            statusform.save(commit=True)
            return redirect("artistworks-page", pk=pk)
        else:
            print("An Error occured")

    content = {"artist": artist,
               "artists": artists,
               "works": works,
               "statusform": statusform,
               }

    return render(request, "databank/index.html", content)


# def artistworks_page(request, pk):
#     artists = Artist.objects.all()
#     artist = Artist.objects.get(pk=pk)
#     works = Work.objects.filter(artist__id=pk)
#     sales = SalesData.objects.filter(work__artist_id=pk)
#     statusform = SalesDataForm()

#     if request.method == "POST":
#         statusform = SalesDataForm(request.POST)
#         if statusform.is_valid():
#             statusform.save(commit=True)
#             return redirect("artistworks-page", pk=pk)

#     content = {"artist": artist,
#                "artists": artists,
#                "works": works,
#                "sales": sales,
#                "statusform": statusform,

#                }

#     return render(request, "databank/index.html", content)
