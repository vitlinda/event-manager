from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, generics
from rest_framework.permissions import AllowAny
from events.permissions import IsOwnerOrReadOnly
from events.serializers import EventSerializer, UserSerializer, RegisterSerializer
from events.models import Event


class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User viewset for `list` and `detail` a .
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
