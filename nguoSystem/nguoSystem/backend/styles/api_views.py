from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Style
from .serializers import StyleSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_style_list(request):
    """List all styles with optional filters."""
    styles = Style.objects.all().order_by('-created_at')

    gender = request.query_params.get('gender')
    category = request.query_params.get('category')
    search = request.query_params.get('search')

    if gender:
        styles = styles.filter(gender=gender)
    if category:
        styles = styles.filter(category=category)
    if search:
        styles = styles.filter(name__icontains=search)

    serializer = StyleSerializer(styles, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_style_detail(request, pk):
    """Get a single style."""
    try:
        style = Style.objects.get(pk=pk)
    except Style.DoesNotExist:
        return Response({'error': 'Mtindo haujapatikana'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StyleSerializer(style, context={'request': request})
    return Response(serializer.data)


class IsTailor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_approved


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_create_style(request):
    """Create a new style (tailor only)."""
    serializer = StyleSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_update_style(request, pk):
    """Update a style (tailor only)."""
    try:
        style = Style.objects.get(pk=pk)
    except Style.DoesNotExist:
        return Response({'error': 'Mtindo haujapatikana'}, status=status.HTTP_404_NOT_FOUND)
    serializer = StyleSerializer(style, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, IsTailor])
def api_delete_style(request, pk):
    """Delete a style (tailor only)."""
    try:
        style = Style.objects.get(pk=pk)
    except Style.DoesNotExist:
        return Response({'error': 'Mtindo haujapatikana'}, status=status.HTTP_404_NOT_FOUND)
    style.delete()
    return Response({'message': 'Mtindo umefutwa'}, status=status.HTTP_204_NO_CONTENT)
