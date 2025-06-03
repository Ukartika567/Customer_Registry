from django.urls import path, include
from .import views

urlpatterns=[
	##User registration and authentication
  	path('api/register/', views.UserRegistrationAPIView.as_view(), name='register'),
	path('api/token/', views.LoginAPIView.as_view(), name='login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='logout'),
]