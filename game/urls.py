from django.urls import path, include
from game.views import *

urlpatterns = [
    path("", index),
    path("game/<int:id>/<str:name>/", game),
    path("", gameAI),
    path('ai_move/', ai_move)
]