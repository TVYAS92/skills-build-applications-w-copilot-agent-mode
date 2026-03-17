from django.contrib import admin
from .models import Team, Activity, WorkoutSuggestion

admin.site.register(Team)
admin.site.register(Activity)
admin.site.register(WorkoutSuggestion)
