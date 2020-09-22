from django.db import models
from django.utils import timezone

class StartTrade(models.Model):
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of the date."""
        date = timezone.localtime(self.log_date)
        return f"logged on {date.strftime('%A, %d %B, %Y at %X')}"