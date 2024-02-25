from django.urls import re_path, path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from events import views
from events.views import EventViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

event_list = EventViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'get': 'my_events'
})
event_detail = EventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
    'post': 'register_for_event',
    'post': 'unregister_from_event'
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

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
