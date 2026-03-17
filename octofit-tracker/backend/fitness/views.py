
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Activity, Team, WorkoutSuggestion
from .serializers import ActivitySerializer, TeamSerializer, UserSerializer, WorkoutSuggestionSerializer

User = get_user_model()

class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

from .models import Activity, Team, WorkoutSuggestion
from .serializers import ActivitySerializer, TeamSerializer, UserSerializer, WorkoutSuggestionSerializer

User = get_user_model()


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().prefetch_related('members')
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        team = serializer.save(owner=self.request.user)
        team.members.add(self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join(self, request, pk=None):
        team = self.get_object()
        team.members.add(request.user)
        serializer = self.get_serializer(team)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().select_related('user', 'team')
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs.order_by('-happened_at')


class WorkoutSuggestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkoutSuggestion.objects.all().order_by('-created_at')
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticated]


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        users = User.objects.annotate(total_points=Sum('activities__duration_minutes*0.5 + activities__distance_km*2 + activities__calories_burned*0.1')).order_by('-total_points')[:20]
        data = [{'id': u.id, 'username': u.username, 'total_points': u.total_points or 0} for u in users]
        return Response(data)

    @action(detail=False, methods=['get'])
    def activity_summary(self, request):
        total_activities = Activity.objects.filter(user=request.user).count()
        total_distance = Activity.objects.filter(user=request.user).aggregate(total=Sum('distance_km'))['total'] or 0
        total_duration = Activity.objects.filter(user=request.user).aggregate(total=Sum('duration_minutes'))['total'] or 0
        return Response({
            'total_activities': total_activities,
            'total_distance_km': total_distance,
            'total_duration_minutes': total_duration,
        })
