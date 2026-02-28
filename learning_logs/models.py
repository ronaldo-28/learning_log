# learning_logs/models.py
from django.db import models
from django.contrib.auth.models import User # Assuming Topic has an owner

class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class Entry(models.Model):
    """Something specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a simple string representing the entry."""
        # This is where the logic needs to be correct
        if len(self.text) > 50:
            return f"{self.text[:50]}..." # Take the first 50 chars and add ellipsis
        else:
            return self.text # Return the full text if 50 chars or less