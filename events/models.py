from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    location = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='events', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']
