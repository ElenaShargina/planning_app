from django.db import models
from django.contrib.auth.models import User
from django.utils.timesince import timesince


class Plan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
    
    @property
    def duration(self):
        """
        Returns the time taken to complete the task.
        Returns None if task is not completed.
        Returns a human-readable string (e.g., "2 hours, 15 minutes").
        """
        if self.status == 'completed' and self.completed_at and self.created_at:
            return timesince(self.created_at, self.completed_at)
        return None

class FlashCardCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_collections')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class FlashCard(models.Model):
    collection = models.ForeignKey(FlashCardCollection, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(max_length=200)
    front_side = models.TextField()
    back_side = models.TextField()

    def __str__(self):
        return self.title