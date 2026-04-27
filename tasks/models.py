from django.db import models
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.utils import timezone

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
        if self.status == 'completed' and self.completed_at and self.created_at:
            return timesince(self.created_at, self.completed_at)
        return None


class FlashCardCollection(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='flashcard_collections'
    )
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title or ''


class FlashCard(models.Model):
    collection = models.ForeignKey(
        FlashCardCollection, on_delete=models.CASCADE, related_name='cards'
    )
    title = models.CharField(max_length=200, blank=True, null=True)
    front_side = models.TextField()
    back_side = models.TextField()

    def __str__(self):
        return self.title or ''


class Timer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timers')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_running(self):
        return self.completed_at is None

    def __str__(self):
        return self.title
    
class DailyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_reports')
    report_date = models.DateField()
    total_time_seconds = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'report_date')
        ordering = ['-report_date']
        verbose_name = 'Ежедневный отчет'
        verbose_name_plural = 'Ежедневные отчеты'

    def __str__(self):
        return f"{self.user.username} | {self.report_date}"

    @property
    def formatted_time(self):
        h = self.total_time_seconds // 3600
        m = (self.total_time_seconds % 3600) // 60
        s = self.total_time_seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @classmethod
    def generate_for_date(cls, user, date_obj):
        tasks = Task.objects.filter(
            plan__user=user,
            status='completed',
            created_at__date=date_obj,
            completed_at__date=date_obj
        )
        
        total_sec = sum(
            int((t.completed_at - t.created_at).total_seconds()) 
            for t in tasks if t.completed_at and t.created_at
        )
        
        cls.objects.update_or_create(
            user=user, 
            report_date=date_obj,
            defaults={'total_time_seconds': total_sec}
        )
        
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    bookmark_date = models.DateField(auto_now_add=True, verbose_name="Дата добавления")
    url = models.URLField(verbose_name="Ссылка")
    title = models.CharField(max_length=250, verbose_name="Название")
    
    class Meta:
        ordering = ['-bookmark_date', '-id']
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'

    def __str__(self):
        return self.title
