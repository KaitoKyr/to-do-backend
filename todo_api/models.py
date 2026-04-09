from django.db import models

# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tasks(models.Model):
    content = models.CharField()
    completed = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)

    def __str__(self):
        return self.content