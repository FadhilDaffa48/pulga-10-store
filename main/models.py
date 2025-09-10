from django.db import models
import uuid
# Create your models here.
class Product(models.Model):
    choices = {
        ('Shoes', 'shoes'),
        ('Jerseys', 'jerseys'),
        ('Miniatures', 'miniatures'),
        ('Posters', 'posters'),
    }
    
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=choices)
    is_featured = models.BooleanField(default=False)