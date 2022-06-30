from django.urls import path

from .views import JoinAuthorView

urlpatterns = [
    path("join/", JoinAuthorView.as_view()),
]
