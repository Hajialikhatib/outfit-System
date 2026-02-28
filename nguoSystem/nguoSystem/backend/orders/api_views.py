from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count
from .models import Order, Comment, CustomStyleRequest
from .serializers import OrderSerializer, CommentSerializer, CustomStyleRequestSerializer
from styles.models import Style
from accounts.models import User
from accounts.serializers import UserSerializer


class IsTailor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_approved


# ─── Orders ───

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_create_order(request, style_id):
    """Create a new order for a specific style."""
    try:
        style = Style.objects.get(pk=style_id)
    except Style.DoesNotExist:
        return Response({'error': 'Mtindo haujapatikana'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, style=style, status='PENDING')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_my_orders(request):
    """Get current user's orders."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_order_detail(request, order_id):
    """Get order detail."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Oda haijapatikana'}, status=status.HTTP_404_NOT_FOUND)

    if order.user != request.user and not request.user.is_staff:
        return Response({'error': 'Huna ruhusa'}, status=status.HTTP_403_FORBIDDEN)

    serializer = OrderSerializer(order, context={'request': request})
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def api_delete_order(request, order_id):
    """Delete an order (within 3 days)."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Oda haijapatikana'}, status=status.HTTP_404_NOT_FOUND)

    if order.user != request.user:
        return Response({'error': 'Huna ruhusa'}, status=status.HTTP_403_FORBIDDEN)

    if not order.can_delete():
        return Response(
            {'error': 'Oda hii haiwezi kufutwa. Siku 3 zimepita.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    order.delete()
    return Response({'message': 'Oda imefutwa'}, status=status.HTTP_204_NO_CONTENT)


# ─── Tailor Dashboard ───

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_tailor_dashboard(request):
    """Get orders for tailor dashboard."""
    orders = Order.objects.all().order_by('-created_at')
    return Response({
        'pending': OrderSerializer(orders.filter(status='PENDING'), many=True, context={'request': request}).data,
        'approved': OrderSerializer(orders.filter(status='APPROVED'), many=True, context={'request': request}).data,
        'rejected': OrderSerializer(orders.filter(status='REJECTED'), many=True, context={'request': request}).data,
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_approve_order(request, order_id):
    """Approve an order."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Oda haijapatikana'}, status=status.HTTP_404_NOT_FOUND)
    order.status = 'APPROVED'
    order.save()
    return Response(OrderSerializer(order, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_reject_order(request, order_id):
    """Reject an order."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Oda haijapatikana'}, status=status.HTTP_404_NOT_FOUND)
    order.status = 'REJECTED'
    order.save()
    return Response(OrderSerializer(order, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_add_comment(request, order_id):
    """Add/update comment on an order."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Oda haijapatikana'}, status=status.HTTP_404_NOT_FOUND)

    message = request.data.get('message')
    if not message:
        return Response({'error': 'Tafadhali andika ujumbe'}, status=status.HTTP_400_BAD_REQUEST)

    comment, _ = Comment.objects.get_or_create(order=order)
    comment.message = message
    comment.save()
    return Response(CommentSerializer(comment).data)


# ─── Custom Style Requests ───

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_create_custom_style_request(request):
    """Create a custom style request."""
    serializer = CustomStyleRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, status='PENDING')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_my_custom_style_requests(request):
    """Get current user's custom style requests."""
    requests = CustomStyleRequest.objects.filter(user=request.user).order_by('-created_at')
    serializer = CustomStyleRequestSerializer(requests, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_custom_style_request_detail(request, request_id):
    """Get custom style request detail."""
    try:
        style_request = CustomStyleRequest.objects.get(pk=request_id)
    except CustomStyleRequest.DoesNotExist:
        return Response({'error': 'Ombi halijapatikana'}, status=status.HTTP_404_NOT_FOUND)

    if style_request.user != request.user and not request.user.is_staff:
        return Response({'error': 'Huna ruhusa'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CustomStyleRequestSerializer(style_request, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_manage_custom_style_requests(request):
    """Admin: list all custom style requests."""
    requests = CustomStyleRequest.objects.all().order_by('-created_at')
    serializer = CustomStyleRequestSerializer(requests, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_approve_custom_style_request(request, request_id):
    """Approve a custom style request."""
    try:
        style_request = CustomStyleRequest.objects.get(pk=request_id)
    except CustomStyleRequest.DoesNotExist:
        return Response({'error': 'Ombi halijapatikana'}, status=status.HTTP_404_NOT_FOUND)

    style_request.status = 'APPROVED'
    estimated_price = request.data.get('estimated_price')
    if estimated_price:
        style_request.estimated_price = estimated_price
    style_request.admin_notes = request.data.get('admin_notes', '')
    style_request.save()
    return Response(CustomStyleRequestSerializer(style_request, context={'request': request}).data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_reject_custom_style_request(request, request_id):
    """Reject a custom style request."""
    try:
        style_request = CustomStyleRequest.objects.get(pk=request_id)
    except CustomStyleRequest.DoesNotExist:
        return Response({'error': 'Ombi halijapatikana'}, status=status.HTTP_404_NOT_FOUND)

    style_request.status = 'REJECTED'
    style_request.admin_notes = request.data.get('admin_notes', '')
    style_request.save()
    return Response(CustomStyleRequestSerializer(style_request, context={'request': request}).data)


# ─── Admin Dashboard ───

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_admin_dashboard(request):
    """Admin dashboard stats."""
    if not request.user.is_staff:
        return Response({'error': 'Huna ruhusa'}, status=status.HTTP_403_FORBIDDEN)

    from feedback.models import Feedback

    data = {
        'total_users': User.objects.filter(is_staff=False).count(),
        'total_tailors': User.objects.filter(is_staff=True, is_superuser=False).count(),
        'total_styles': Style.objects.count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='PENDING').count(),
        'approved_orders': Order.objects.filter(status='APPROVED').count(),
        'rejected_orders': Order.objects.filter(status='REJECTED').count(),
        'pending_custom_requests': CustomStyleRequest.objects.filter(status='PENDING').count(),
        'total_feedbacks': Feedback.objects.count(),
        'recent_orders': OrderSerializer(
            Order.objects.all().order_by('-created_at')[:10],
            many=True, context={'request': request}
        ).data,
    }
    return Response(data)
