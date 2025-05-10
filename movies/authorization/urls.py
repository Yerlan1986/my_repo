from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authorization import views

urlpatterns = [
    path('health/', views.HealthApiView.as_view()),
    path('me/', views.MeAPIView.as_view()),
    path('register/', views.RegisterAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
    path('me/update/', views.UpdateUserAPIView.as_view()),
    path('me/delete/', views.DeleteUserAPIView.as_view()),
    path('me/change-password/', views.ChangePasswordAPIView.as_view()),
    path('user/list/', views.UserListAPIView.as_view()),
]



