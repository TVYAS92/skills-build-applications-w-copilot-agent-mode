"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


from fitness.views import TeamViewSet, ActivityViewSet, WorkoutSuggestionViewSet, DashboardViewSet, UserViewSet


router = DefaultRouter()
router.register('teams', TeamViewSet, basename='team')
router.register('activities', ActivityViewSet, basename='activity')
router.register('workout-suggestions', WorkoutSuggestionViewSet, basename='workoutsuggestion')
router.register('dashboard', DashboardViewSet, basename='dashboard')
router.register('users', UserViewSet, basename='user')


import os

@api_view(['GET'])
def api_root(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = request.build_absolute_uri('/')[:-1]
    return Response({
        'teams': f"{base_url}/api/teams/",
        'activities': f"{base_url}/api/activities/",
        'workout-suggestions': f"{base_url}/api/workout-suggestions/",
        'dashboard': f"{base_url}/api/dashboard/",
        'auth': f"{base_url}/api/auth/login/",
        'registration': f"{base_url}/api/auth/registration/",
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
