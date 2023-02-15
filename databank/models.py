from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    factor = models.IntegerField(blank=True)

    def __str__(self) -> str:
        return f"{self.name}, {self.factor}"


class Work(models.Model):
    STORAGE_TAG = "ausstehend"

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True)

    storage_tag = models.CharField(
        blank=True, default=STORAGE_TAG, max_length=100)

    image = models.ImageField(
        upload_to="artist_images", unique=True, blank=True)
    name = models.CharField(max_length=300, blank=True)
    production_date = models.IntegerField(default=None, blank=True)
    materials = models.CharField(max_length=300, blank=True)

    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    depth = models.IntegerField(blank=True, default=0)

    price = models.IntegerField(blank=True, default=0)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self) -> str:
        return f"{self.artist}, {self.name}"


class Status(models.Model):
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
        STORED = "Gelagert", "Gelagert"
        SOLD = "Verkauft", "Verkauft"

    work = models.OneToOneField(
        Work, on_delete=models.PROTECT, blank=True)

    date = models.DateField(null=True)
    buyer = models.CharField(max_length=100, blank=True, null=True)
    tax = models.IntegerField(
        choices=TaxChoice.choices, default=TaxChoice.NINETEEN, blank=True)
    decree = models.IntegerField(
        choices=DecreeChoice.choices, default=DecreeChoice.ZERO, blank=True)
    status = models.CharField(choices=StorageStatus.choices,
                              default=StorageStatus.STORED, max_length=20, blank=True)

    def __str__(self):
        return f"{self.date}, {self.buyer}"
