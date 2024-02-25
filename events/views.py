from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from events.permissions import IsOwnerOrReadOnly
from events.serializers import EventSerializer, RegisterSerializer
from events.models import Event
import django_filters.rest_framework


class RegisterView(generics.CreateAPIView):
    """
    This view allows users to register a new account by providing their
    username, email, and password. The registration process creates a new
    User object in the database.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class EventFilter(django_filters.FilterSet):
    """
    This filter allows users to retrieve events based on whether they have
    already occurred or are scheduled for the future. It provides a boolean
    filter field 'is_past_event'.
    """
    is_past_event = django_filters.BooleanFilter(method='filter_is_past_event')

    class Meta:
        model = Event
        fields = ['is_past_event']

    def filter_is_past_event(self, queryset, name, value):
        today = timezone.now()
        if value:
            return queryset.filter(start_date__lt=today)
        else:
            return queryset.filter(start_date__gte=today)


class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset provides CRUD operations for managing events. It allows users
    to list, create, retrieve, update, and delete events. It also provides
    additional actions for registering and unregistering users from events and 
    for retrieving all the events created by the authenticated user.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (
        permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = EventFilter

    def perform_create(self, serializer):
        """
        This method is called when creating a new event. It sets the owner of
        the event to the authenticated user.
        """
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def my_events(self, request):
        """
        This action allows an authenticated user to retrieve all the events they have created.
        """
        user = request.user
        events = Event.objects.filter(owner=user)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register_for_event(self, request, pk=None):
        """
        This action allows an authenticated user to register for a future event.
        It checks if the event is in the future and if the event has reached its
        capacity before registering the user.
        """
        event = self.get_object()

        # Check if the event is in the future
        if not event.is_in_future():
            return Response({'detail': 'Cannot register to past events.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the event has reached its capacity
        if event.attendees.count() >= event.capacity:
            return Response({'detail': 'Event capacity reached. Cannot register more users.'}, status=status.HTTP_400_BAD_REQUEST)

        # Register the authenticated user for the event
        user = request.user
        event.attendees.add(user)
        return Response({'detail': 'Successfully registered for the event.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unregister_from_event(self, request, pk=None):
        """
        This action allows an authenticated user to unregister from an event
        they have previously registered for.
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
