from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(
        read_only=True
    )  # Use is_staff instead of is_admin

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "is_staff",  # Use is_staff to check for admin status
        ]

    def create(self, validated_data):
        # Use the default create method for the built-in User model
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user
