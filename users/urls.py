from django.urls import path

from .views import RegistrationView, ChangePasswordView, MeView


urlpatterns = [
    path('users/reg/', RegistrationView.as_view(), name='reg'),
    path('users/change-passwd/', ChangePasswordView.as_view(), name='change_passwd'),
    path('users/me/', MeView.as_view(), name='me'),
]
