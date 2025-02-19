from django.db import models
from django.utils.timesince import timesince

class Network(models.Model):
    name = models.CharField(max_length=100)
    ussid = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} Network ---> {self.ussid}"

class Command(models.Model):
    target = models.CharField(max_length=100, blank=True,null=True)
    command = models.CharField(max_length=100, blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.command} waiting for excution on {self.target} at {timesince(self.created)} ago"

    class Meta:
        ordering = ['-created']

class State(models.Model):
    target = models.CharField(max_length=100, blank=True,null=True)
    state = models.CharField(max_length=100, blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.state} for {self.target} at {timesince(self.created)} ago"

class Log(models.Model):
    target = models.CharField(max_length=100, blank=True,null=True)
    log = models.TextField()
    img = models.FileField(upload_to="media/",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f" {self.id} | {self.target} respond at {timesince(self.created)} ago"
    
    def get_created_at(self, instance):
            return timesince(instance.created_at) + " ago"

    class Meta:
        ordering = ['-created']
    

class Target(models.Model):
    name = models.CharField(max_length=50)
    ip = models.CharField(max_length=20)
    os_name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created']