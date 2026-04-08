from django.db import models

# Create your models here.

class Tasks(models.Model):
    content = models.CharField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.content