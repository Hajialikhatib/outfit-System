from django.urls import path
from . import api_views

urlpatterns = [
    # Orders
    path('create/<int:style_id>/', api_views.api_create_order, name='api_create_order'),
    path('my-orders/', api_views.api_my_orders, name='api_my_orders'),
    path('<int:order_id>/', api_views.api_order_detail, name='api_order_detail'),
    path('<int:order_id>/delete/', api_views.api_delete_order, name='api_delete_order'),
    path('<int:order_id>/comment/', api_views.api_add_comment, name='api_add_comment'),
    path('<int:order_id>/approve/', api_views.api_approve_order, name='api_approve_order'),
    path('<int:order_id>/reject/', api_views.api_reject_order, name='api_reject_order'),

    # Tailor / Admin
    path('dashboard/', api_views.api_tailor_dashboard, name='api_tailor_dashboard'),
    path('admin-dashboard/', api_views.api_admin_dashboard, name='api_admin_dashboard'),

    # Custom Style Requests
    path('custom-style/create/', api_views.api_create_custom_style_request, name='api_create_csr'),
    path('custom-style/my/', api_views.api_my_custom_style_requests, name='api_my_csr'),
    path('custom-style/<int:request_id>/', api_views.api_custom_style_request_detail, name='api_csr_detail'),
    path('custom-style/manage/', api_views.api_manage_custom_style_requests, name='api_manage_csr'),
    path('custom-style/<int:request_id>/approve/', api_views.api_approve_custom_style_request, name='api_approve_csr'),
    path('custom-style/<int:request_id>/reject/', api_views.api_reject_custom_style_request, name='api_reject_csr'),
]
