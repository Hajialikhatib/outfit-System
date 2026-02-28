from rest_framework import serializers
from .models import Feedback
from orders.serializers import OrderSerializer
from accounts.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    order_detail = OrderSerializer(source='order', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'user_detail', 'order', 'order_detail',
            'message', 'rating', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
