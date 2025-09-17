from django.forms import ModelForm
from main import models

class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['name',  'category', 'price', 'description', 'thumbnail']
