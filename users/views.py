from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.serializers import UserSerializer  # Import the serializer
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    serializer = UserSerializer(
        user
    )  # Use the UserSerializer to serialize the user instance
    return Response(serializer.data)  # Return serialized data


@api_view(["POST"])
@permission_classes([AllowAny])  # Allow access to unauthenticated users
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"success": "User created successfully", "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User login view
@api_view(["POST"])
@permission_classes([AllowAny])  # Allow access to unauthenticated users
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)  # Authenticate the user

    if user is not None:
        # Generate or retrieve a token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,  # Include the username in the response
            }
        )
    else:
        return Response(
            {"error": "Invalid user or password"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def logout(request):
    try:
        token = (
            request.auth
        )  # The token is automatically parsed by the token authentication
        if token:
            token.delete()  # Delete the token, effectively logging the user out
            return Response(
                {"success": "Logged out successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Token not provided"}, status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {"error": f"Logout failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
        )
