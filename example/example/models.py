from django.db import models


class MyModel(models.Model):
    created = models.DateTimeField("created")
    name = models.CharField("name", max_length=30)
    birthday = models.DateField("birthday")
    number = models.IntegerField("number")
    STATUS_CHOICES = [(i, i) for i in range(1, 11)]
    status = models.IntegerField("status", choices=STATUS_CHOICES)

