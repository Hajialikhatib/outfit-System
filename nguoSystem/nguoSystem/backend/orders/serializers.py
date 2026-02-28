from rest_framework import serializers
from .models import Order, Comment, CustomStyleRequest
from styles.serializers import StyleSerializer
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'order', 'message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    style_detail = StyleSerializer(source='style', read_only=True)
    user_detail = UserSerializer(source='user', read_only=True)
    comment = CommentSerializer(read_only=True)
    can_delete = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'style', 'style_detail', 'user_detail',
            'custom_style', 'size', 'status',
            'kifua', 'mkono', 'kiuno', 'mguu', 'urefu', 'shingo',
            'total_price', 'delivery_date',
            'created_at', 'updated_at', 'comment', 'can_delete'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']

    def get_can_delete(self, obj):
        return obj.can_delete()


class CustomStyleRequestSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomStyleRequest
        fields = [
            'id', 'user', 'user_detail', 'image', 'image_url',
            'description', 'preferred_fabric', 'estimated_price',
            'status', 'admin_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
