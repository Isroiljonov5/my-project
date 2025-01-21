import datetime 
from django.db import models
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
        
    class Meta:
        ordering = ['-id']
        
    
    def get_published_days(self):
        _now = datetime.datetime.now()
        days = _now.date() - self.created_at.date()
        if days.days > 365:
            return days
        if days.days == 0:
            return " Posted Today !"
        elif days.days == 1:
            return " Posted Yesterday !"
        else:
            return f" Posted {days.days} days ago !"
    
    def __str__(self):
        return self.title
    