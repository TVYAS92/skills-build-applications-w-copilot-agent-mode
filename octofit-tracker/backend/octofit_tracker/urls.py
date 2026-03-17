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

from fitness.views import TeamViewSet, ActivityViewSet, WorkoutSuggestionViewSet, DashboardViewSet

router = DefaultRouter()
router.register('teams', TeamViewSet, basename='team')
router.register('activities', ActivityViewSet, basename='activity')
router.register('workout-suggestions', WorkoutSuggestionViewSet, basename='workoutsuggestion')
router.register('dashboard', DashboardViewSet, basename='dashboard')

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'teams': reverse('team-list', request=request, format=format),
        'activities': reverse('activity-list', request=request, format=format),
        'workout-suggestions': reverse('workoutsuggestion-list', request=request, format=format),
        'dashboard': reverse('dashboard-list', request=request, format=format),
        'auth': reverse('rest_login', request=request, format=format),
        'registration': reverse('dj-rest-auth:registration', request=request, format=format),
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]
