from django.db import models
from django.db.models import Model
from ckeditor.fields import RichTextField
# RichTextField() for customizable text

# Create your models here.

class Renter(models.Model):
    name = models.CharField(max_length=100, blank=True, default="")
    company_name = models.CharField(max_length=100, blank=True, default="")
    address = models.CharField(max_length=100, blank=True, default="")
    plz = models.CharField(max_length=100, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")

    slug = models.SlugField(unique=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}, {self.company_name}"



class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    factor = models.IntegerField(blank=True, default=0)
    storagetag = models.CharField(max_length=5, unique=True, default="")
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}, {self.factor}"


class Work(models.Model):

    class TaxChoice(models.IntegerChoices):
        NINETEEN = 19, "19"
        SEVEN = 7, "7"


    class DecreeChoice(models.IntegerChoices):
        ZERO = 0, "0"
        FIVE = 5, "5"
        TEN = 10, "10"
        FIFTEEN = 15, "15"
        TWENTY = 20, "20"


    class StorageStatus(models.TextChoices):
        WPT = "Wuppertal", "Wuppertal"
        NUG = "Nah&Gut", "Nah&Gut"
        DDORF = "Düsseldorf", "Düsseldorf"
        RNT = "Vermietet", "Vermietet"
        OUT = "Abgegeben", "Abgegeben"


    class SalesStatus(models.TextChoices):
        SOLD = "Verkauft", "Verkauft"
        GLVT = "Geliefert", "Geliefert"
        

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True)

    image = models.ImageField(
        upload_to="artist_images", unique=True, blank=True, default="default.png")
    name = models.CharField(max_length=300, blank=True)
    production_date = models.IntegerField(default=None, blank=True)
    materials = models.CharField(max_length=300, blank=True)

    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    depth = models.IntegerField(blank=True, default=0)

    price = models.IntegerField(blank=True, default=0)
    
    renter = models.ForeignKey(
        Renter, on_delete=models.SET_NULL, blank=True, null=True)
    
    
    slug = models.SlugField(unique=True, blank=True)



    salesdate = models.DateField(null=True, blank=True)
    buyer = models.CharField(max_length=100, blank=True, null=True)
    tax = models.IntegerField(
        choices=TaxChoice.choices, default=TaxChoice.NINETEEN, blank=True, null=True)
    decree = models.IntegerField(
        choices=DecreeChoice.choices, default=DecreeChoice.ZERO, blank=True, null=True)
    storagestatus = models.CharField(choices=StorageStatus.choices,
                                     default=StorageStatus.WPT, max_length=20, blank=True)
    salesstatus = models.CharField(choices=SalesStatus.choices,
                                   default="", max_length=20, blank=True)


    def __str__(self) -> str:
        return f"{self.artist}, {self.name}"
