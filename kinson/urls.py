from django.urls import path
from . import issue

urlpatterns = [
    path('issue', issue.issue.as_view()),
]