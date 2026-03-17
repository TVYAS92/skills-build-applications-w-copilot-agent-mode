from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from fitness.models import Team, Activity, WorkoutSuggestion

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Deleting old data...'))
        Activity.objects.all().delete()
        Team.objects.all().delete()
        WorkoutSuggestion.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Team Marvel', description='Earth’s mightiest heroes', owner=None)
        dc = Team.objects.create(name='Team DC', description='Justice League and friends', owner=None)

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark', 'team': marvel},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers', 'team': marvel},
            {'username': 'spiderman', 'email': 'spidey@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker', 'team': marvel},
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne', 'team': dc},
            {'username': 'superman', 'email': 'superman@dc.com', 'first_name': 'Clark', 'last_name': 'Kent', 'team': dc},
            {'username': 'wonderwoman', 'email': 'diana@dc.com', 'first_name': 'Diana', 'last_name': 'Prince', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(username=u['username'], email=u['email'], first_name=u['first_name'], last_name=u['last_name'], password='password123')
            u['team'].members.add(user)
            if not u['team'].owner:
                u['team'].owner = user
                u['team'].save()
            user_objs.append(user)

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=user_objs[0], team=marvel, activity_type='run', duration_minutes=30, distance_km=5, calories_burned=400)
        Activity.objects.create(user=user_objs[1], team=marvel, activity_type='bike', duration_minutes=60, distance_km=20, calories_burned=800)
        Activity.objects.create(user=user_objs[2], team=marvel, activity_type='swim', duration_minutes=45, distance_km=2, calories_burned=350)
        Activity.objects.create(user=user_objs[3], team=dc, activity_type='walk', duration_minutes=50, distance_km=4, calories_burned=250)
        Activity.objects.create(user=user_objs[4], team=dc, activity_type='gym', duration_minutes=90, distance_km=0, calories_burned=700)
        Activity.objects.create(user=user_objs[5], team=dc, activity_type='other', duration_minutes=20, distance_km=1, calories_burned=120)

        self.stdout.write(self.style.SUCCESS('Creating workout suggestions...'))
        WorkoutSuggestion.objects.create(title='5K Run', description='A simple 5 kilometer run.', difficulty='easy', tags='run,cardio')
        WorkoutSuggestion.objects.create(title='HIIT Session', description='High intensity interval training.', difficulty='hard', tags='hiit,gym')
        WorkoutSuggestion.objects.create(title='Swim Laps', description='Swim 20 laps in the pool.', difficulty='medium', tags='swim,cardio')

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
