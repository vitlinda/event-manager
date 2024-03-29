from django.utils import timezone
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    attendees = models.ManyToManyField('auth.User')
    owner = models.ForeignKey(
        'auth.User', related_name='events', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    capacity = models.PositiveIntegerField(default=3)

    class Meta:
        ordering = ['created']

    def is_in_future(self):
        """
        Check if an event is in the future.

        Returns:
            bool: True if the event is in the future, False otherwise.
        """
        return self.start_date > timezone.now()
