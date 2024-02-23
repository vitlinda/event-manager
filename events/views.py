from datetime import timezone
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions, viewsets, generics, status
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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register_for_event(self, request, pk=None):
        """
        Register an authenticated user for a future event.
        """
        event = self.get_object()

        # Check if the event is in the future
        if not event.is_in_future():
            return Response({'detail': 'Cannot register to past events.'}, status=status.HTTP_400_BAD_REQUEST)

        # Register the authenticated user for the event
        user = request.user
        event.attendees.add(user)
        return Response({'detail': 'Successfully registered for the event.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unregister_from_event(self, request, pk=None):
        """
        Unregister the authenticated user from the event.
        """
        event = self.get_object()

        # Get the authenticated user
        user = request.user

        # Check if the user is registered for the event
        if user in event.attendees.all():
            # Remove the user from the attendees list
            event.attendees.remove(user)
            return Response({'detail': 'Successfully unregistered from the event.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'User is not registered for the event.'}, status=status.HTTP_400_BAD_REQUEST)
