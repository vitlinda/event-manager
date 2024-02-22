from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events import views
from events.views import EventViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)

event_list = EventViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
event_detail = EventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('events/',
         event_list,
         name='events-list'),
    path('events/<int:pk>/',
         event_detail,
         name='event-detail'),
]

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')

# The API URLs are determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
