from django.urls import path
from . import api_views

urlpatterns = [
    path('submit/<int:order_id>/', api_views.api_submit_feedback, name='api_submit_feedback'),
    path('my/', api_views.api_my_feedbacks, name='api_my_feedbacks'),
    path('all/', api_views.api_all_feedbacks, name='api_all_feedbacks'),
]
