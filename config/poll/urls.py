from django.urls import path
from . import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("question/", views.QuestionView.as_view(), name='question'),
    path("choice/", views.ChoiceView.as_view(), name='choice'),
    path("vote/<int:qid>/", views.VoteView.as_view(), name='vote'),
    path("result/<int:qid>/", views.ResultView.as_view(), name='result'),
]

