"""
Users URL configuration for tcc_control project.
"""

from django.urls import path

from users.views import SignUpView, UserListView, ProfileDetailView


app_name = 'users'
urlpatterns = [
    path('create/', SignUpView.as_view(), name='signup'),
    path('<uuid:pk>/profile/', ProfileDetailView.as_view(), name='profile'),
    path('list/', UserListView.as_view(), name='list'),
]
