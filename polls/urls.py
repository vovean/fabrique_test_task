from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from polls.views import polls, questions

router = DefaultRouter()
router.register('polls', viewset=polls.PollViewSet)
router.register('questions', viewset=questions.QuestionViewSet, basename='questions')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.obtain_auth_token)
]
