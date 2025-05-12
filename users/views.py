from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .serializers import SignUpSerializer

@api_view(['POST'])
def signup_view(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'message': 'Login successful!'
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()  # delete the current token
    return Response({'message': 'Logged out successfully!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail_view(request):
    serializer = SignUpSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)