from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import serializers

from .models import UserRole

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "full_name", "rank",
            "course_num", "role", "battalion", "platoon", "team",
            "must_change_password",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=10, write_only=True)
    confirm_password = serializers.CharField(min_length=10, write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Used for commander-created users.
    The creator provides only what they are allowed to provide.
    Auto-filled fields are applied in the view.
    """
    temp_password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "rank",
            "role",
            "course_num",
            "battalion",
            "platoon",
            "team",
            "temp_password",
        ]
        read_only_fields = ["course_num", "battalion", "platoon", "team"]

    def create(self, validated_data):
        temp_password = get_random_string(16)
        user = User.objects.create_user(
            email=validated_data["email"],
            password=temp_password,
            full_name=validated_data["full_name"],
            rank=validated_data["rank"],
            role=validated_data["role"],
            course_num=validated_data["course_num"],
            battalion=validated_data["battalion"],
            platoon=validated_data.get("platoon"),
            team=validated_data.get("team"),
            must_change_password=True,
            is_active=True,
        )
        user.temp_password = temp_password
        return user


class BulkCreateSerializer(serializers.Serializer):
    users = serializers.ListField(child=serializers.DictField(), allow_empty=False)
