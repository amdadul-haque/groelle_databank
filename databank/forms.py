from django import forms
from django.utils.text import slugify

from .models import Work, Artist, Renter


class RenterForm(forms.ModelForm):
    class Meta:
        fields = ["name", "company_name", "address", "plz", "city", "slug"]
        labels = {
            "name": "Name *",
            "company_name": "Firma",
            "address": "Adresse",
            "plz": "PLZ",
            "city": "Ort",
            "slug": "Slug",
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")

        if name:
            slug = slugify(name)
            cleaned_data['slug'] = slug

        return cleaned_data



class ArtistForm(forms.ModelForm):
    class Meta:
        model= Artist
        fields= ["name", "factor", "storagetag", "slug"]
        labels = {
            "factor": "Faktor",
            "storagetag": "Lagerbuchstabe",
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("name")

        if title:
            slug = slugify(title)
            cleaned_data['slug'] = slug

        return cleaned_data


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ["artist", "renter", "image", "name", "production_date", "materials", "width", "height", "depth", "price", "storagestatus", "slug"]
        labels = {
            "artist": "Künstler *",
            "renter": "Mieter",
            "image": "Bild *",
            "name": "Titel *",
            "production_date": "Produktionsdatum *",
            "materials": "Material *",
            "width": "Breite *",
            "height": "Höhe *",
            "depth": "Tiefe",
            "price": "Preis *",
            "storagestatus": "Standort *",
            
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("name")

        if title:
            slug = slugify(title)
            cleaned_data['slug'] = slug

        return cleaned_data




class SaleForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ["salesdate", "buyer", "tax", "decree", "salesstatus",]
        labels = {
            "salesdate": "Verkaufsdatum",
            "buyer": "Käufer *",
            "tax": "Steuersatz",
            "decree": "Erlass",
            "salesstatus": "Verkaufsstatus *",
        }