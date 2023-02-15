from django import forms

from .models import Status, Work


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = "__all__"


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = "__all__"
