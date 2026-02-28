from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from orders.models import Order
from .models import Feedback
from .serializers import FeedbackSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_submit_feedback(request, order_id):
    """Submit feedback for an approved order."""
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Oda haijapatikana'}, status=status.HTTP_404_NOT_FOUND)

    if order.user != request.user:
        return Response({'error': 'Huna ruhusa'}, status=status.HTTP_403_FORBIDDEN)

    if order.status not in ['APPROVED', 'COMPLETED', 'DELIVERED']:
        return Response(
            {'error': 'Unaweza kutoa maoni tu kwa oda zilizokubaliwa'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if hasattr(order, 'feedback'):
        return Response(
            {'error': 'Umeshakutoa maoni kwa oda hii'},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, order=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_my_feedbacks(request):
    """Get current user's feedbacks."""
    feedbacks = Feedback.objects.filter(user=request.user)
    serializer = FeedbackSerializer(feedbacks, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_all_feedbacks(request):
    """Get all feedbacks (admin/tailor only)."""
    if not request.user.is_staff:
        return Response({'error': 'Huna ruhusa'}, status=status.HTTP_403_FORBIDDEN)
    feedbacks = Feedback.objects.all().select_related('user', 'order')
    serializer = FeedbackSerializer(feedbacks, many=True, context={'request': request})
    return Response(serializer.data)
