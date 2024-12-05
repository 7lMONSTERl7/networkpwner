from django.db import models


class Network(models.Model):
    name = models.CharField(max_length=100)
    ussid = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} Network ---> {self.ussid}"
