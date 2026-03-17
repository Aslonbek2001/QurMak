from django.urls import path
from .views import VocabularySearchView
urlpatterns = [
    path('', VocabularySearchView.as_view(), name='vocabulary')
]
