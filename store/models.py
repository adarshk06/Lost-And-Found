from django.db import models

# Create your models here.

class product(models.Model):

    def __str__(self):
        return self.name

    added_by = models.IntegerField()
    name = models.CharField(max_length=500)
    category = models.CharField(max_length=200)
    description = models.TextField(max_length=10000)
    image = models.ImageField(upload_to = 'photos/product', blank = True)
    claimed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
        
    name = models.CharField(max_length=5000)
    address = models.CharField(max_length=10000)
    city = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    email = models.CharField(max_length=500, default="abc@abc.com")
    items = models.CharField(max_length=1000)
    total = models.CharField(max_length=200)