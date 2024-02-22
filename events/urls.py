from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events import views
from events.views import EventViewSet, UserViewSet, RegisterView
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
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('events/',
         event_list,
         name='events-list'),
    path('events/<int:pk>/',
         event_detail,
         name='event-detail'),
    path('users/',
         user_list,
         name='user-list'),
    path('users/<int:pk>/',
         user_detail,
         name='user-detail'),
]

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'users', views.UserViewSet, basename='user')

# The API URLs are determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
]