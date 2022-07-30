from django.urls import path, include
from .views import (
    PostListApiView,
)

urlpatterns = [
    path('posts/', PostListApiView.as_view()),
]