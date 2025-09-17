import uuid
from django.db import models
# Create your models here.
class Product(models.Model):
    choices = {
        ('Shoes', 'Shoes'),
        ('Jerseys', 'Jerseys'),
        ('Miniatures', 'Miniatures'),
        ('Posters', 'Posters'),
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=choices)
    sold = models.IntegerField(default=0)

    @property
    def is_hot(self):
        return self.sold >= 100
    
    def incr_sold(self):
        self.sold += 1
        self.save()