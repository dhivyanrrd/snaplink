from django.urls import path
from .views import RegisterView, ShortenURLView, URLAnalyticsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('shorten/', ShortenURLView.as_view(), name='shorten'),
    path('analytics/<str:short_code>/', URLAnalyticsView.as_view(), name='analytics'),
]