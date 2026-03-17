from django.urls import path
from .views import UserListCreateView, LoginView, LogoutView, UserUpdateView, UserProfileView 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", UserListCreateView.as_view()),
    path("<int:pk>/", UserUpdateView.as_view()),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path("api/token/", LoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("profile", UserProfileView.as_view())
    
]
