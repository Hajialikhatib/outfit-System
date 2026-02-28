from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.api_style_list, name='api_style_list'),
    path('<int:pk>/', api_views.api_style_detail, name='api_style_detail'),
    path('create/', api_views.api_create_style, name='api_create_style'),
    path('<int:pk>/update/', api_views.api_update_style, name='api_update_style'),
    path('<int:pk>/delete/', api_views.api_delete_style, name='api_delete_style'),
]
