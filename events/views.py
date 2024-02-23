from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from events.permissions import IsOwnerOrReadOnly
from events.serializers import EventSerializer, RegisterSerializer
from events.models import Event


class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    Event viewset for `list`, `create`, `retrieve`,
    `update` and `destroy`.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def my_events(self, request):
        """
        Retrieve events created by the authenticated user.
        """
        user = request.user
        events = Event.objects.filter(owner=user)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
