from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserResponseSerializer
)


class RegisterView(APIView):
    """
    Register a new user with name, email, and password.
    Endpoint: POST /api/auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=UserRegisterSerializer,
        responses={
            201: OpenApiResponse(description="User registered successfully"),
            400: OpenApiResponse(description="Validation error"),
        },
        tags=["Authentication"]
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'message': 'User registered successfully.',
                    'user': UserResponseSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Log in an existing user and obtain a JWT access and refresh token.
    Endpoint: POST /api/auth/login/
    """
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(description="Login successful with JWT tokens"),
            400: OpenApiResponse(description="Invalid credentials or bad request"),
        },
        tags=["Authentication"]
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = validated_data['user']
            tokens = validated_data['tokens']
            return Response(
                {
                    'message': 'Login successful.',
                    'user': UserResponseSerializer(user).data,
                    'tokens': tokens
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """
    Get current logged in user details.
    Endpoint: GET /api/auth/me/
    """
    permission_classes = (permissions.IsAuthenticated,)

    @extend_schema(
        responses={200: UserResponseSerializer},
        tags=["Authentication"]
    )
    def get(self, request):
        serializer = UserResponseSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
