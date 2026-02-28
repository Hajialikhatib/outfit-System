from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_register(request):
    """Register a new user and return auth token."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_login(request):
    """Login and return auth token."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            if not user.is_active:
                return Response(
                    {'error': 'Akaunti hii imezimwa'},
                    status=status.HTTP_403_FORBIDDEN
                )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
            })
        return Response(
            {'error': 'Barua pepe au neno la siri si sahihi'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_logout(request):
    """Logout - delete auth token."""
    try:
        request.user.auth_token.delete()
    except Exception:
        pass
    return Response({'message': 'Umetoka kwa mafanikio'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_me(request):
    """Get current user profile."""
    return Response(UserSerializer(request.user).data)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def api_update_profile(request):
    """Update current user profile."""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── Admin: User Management ───
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def api_list_users(request):
    """List all users (admin only)."""
    status_filter = request.query_params.get('status', 'all')
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')

    if status_filter == 'pending':
        users = users.filter(is_approved=False)
    elif status_filter == 'approved':
        users = users.filter(is_approved=True)
    elif status_filter == 'tailors':
        users = users.filter(is_staff=True)
    elif status_filter == 'customers':
        users = users.filter(is_staff=False)

    data = {
        'users': UserSerializer(users, many=True).data,
        'total_users': User.objects.filter(is_superuser=False).count(),
        'pending_users': User.objects.filter(is_superuser=False, is_approved=False).count(),
        'approved_users': User.objects.filter(is_superuser=False, is_approved=True).count(),
        'total_tailors': User.objects.filter(is_staff=True, is_superuser=False).count(),
        'total_customers': User.objects.filter(is_staff=False, is_superuser=False).count(),
    }
    return Response(data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def api_approve_user(request, user_id):
    """Approve a user."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Mtumiaji hajapatikana'}, status=status.HTTP_404_NOT_FOUND)
    user.is_approved = True
    user.save()
    return Response({'message': f'{user.full_name} amekubaliwa', 'user': UserSerializer(user).data})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def api_reject_user(request, user_id):
    """Reject a user."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Mtumiaji hajapatikana'}, status=status.HTTP_404_NOT_FOUND)
    user.is_approved = False
    user.save()
    return Response({'message': f'{user.full_name} amekataliwa', 'user': UserSerializer(user).data})


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def api_delete_user(request, user_id):
    """Delete a user."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Mtumiaji hajapatikana'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({'message': 'Mtumiaji amefutwa'}, status=status.HTTP_204_NO_CONTENT)
