from django.conf import settings
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('run', 'Running'),
        ('bike', 'Cycling'),
        ('swim', 'Swimming'),
        ('walk', 'Walking'),
        ('gym', 'Gym workout'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='activities', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='activities', on_delete=models.SET_NULL, null=True, blank=True)
    activity_type = models.CharField(max_length=32, choices=ACTIVITY_TYPES)
    duration_minutes = models.FloatField(default=0)
    distance_km = models.FloatField(default=0)
    calories_burned = models.FloatField(default=0)
    happened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.activity_type} {self.distance_km}km"

    @property
    def points(self):
        return self.duration_minutes * 0.5 + self.distance_km * 2 + self.calories_burned * 0.1


class WorkoutSuggestion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium')
    tags = models.CharField(max_length=256, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
