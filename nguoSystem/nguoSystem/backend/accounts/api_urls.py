from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.api_register, name='api_register'),
    path('login/', api_views.api_login, name='api_login'),
    path('logout/', api_views.api_logout, name='api_logout'),
    path('me/', api_views.api_me, name='api_me'),
    path('me/update/', api_views.api_update_profile, name='api_update_profile'),

    # Admin User Management
    path('users/', api_views.api_list_users, name='api_list_users'),
    path('users/<int:user_id>/approve/', api_views.api_approve_user, name='api_approve_user'),
    path('users/<int:user_id>/reject/', api_views.api_reject_user, name='api_reject_user'),
    path('users/<int:user_id>/delete/', api_views.api_delete_user, name='api_delete_user'),
]
