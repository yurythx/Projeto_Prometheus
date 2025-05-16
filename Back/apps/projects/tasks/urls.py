from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, LabelViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'labels', LabelViewSet, basename='label')

urlpatterns = [
    path('', include(router.urls)),
]