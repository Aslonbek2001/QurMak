from django.urls import path
from .views import UserLevelPageByLevelView, UserLevelPageByLevelView

urlpatterns = [
    path('data/', UserLevelPageByLevelView.as_view(), name='data')
]
