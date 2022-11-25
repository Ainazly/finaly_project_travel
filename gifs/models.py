from django.db import models
from tours.models import Tour


class Certificate(models.Model):
    tours = models.ForeignKey(Tour, on_delete=models.CASCADE)
    body = models.TextField()
    count_people = models.IntegerField()
    price = models.IntegerField()
    sender = models.CharField(max_length=50)
    addressee = models.CharField(max_length=50)
    

