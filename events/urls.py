from django.urls import re_path, path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from events import views
from events.views import EventViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Event Manager API",
        default_version='v1',
        description="Event Manager API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]
