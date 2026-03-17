from django.urls import path
from .views import BookOneView, BookTwoView

urlpatterns = [
    path("one/", BookOneView.as_view(), name="one"),
    path("two/", BookTwoView.as_view(), name="two"),
]
