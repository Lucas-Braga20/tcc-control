"""
Users URL configuration for tcc_control project.
"""

from django.urls import path

from users.views import SignUpView


app_name = 'users'
urlpatterns = [
    path('create/', SignUpView.as_view(), name='signup'),
]
