from django.forms import ModelForm
from django import forms
from main import models

class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['name',  'category', 'price', 'description', 'thumbnail']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'thumbnail': forms.URLInput(attrs={'class': 'form-control'}),
        }
