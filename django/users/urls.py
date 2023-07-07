"""
Users URL configuration for tcc_control project.
"""

from django.urls import path

from users.views import SignUpView, UserListView


app_name = 'users'
urlpatterns = [
    path('create/', SignUpView.as_view(), name='signup'),
    path('list/', UserListView.as_view(), name='list'),
]
