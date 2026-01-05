from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    MeSerializer,
    ChangePasswordSerializer,
    CreateUserSerializer,
    BulkCreateSerializer,
)
from .permissions import MustChangePasswordBlocker, CanCreateUsers, CAN_CREATE
from .models import UserRole

User = get_user_model()


class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["battalion"] = user.battalion
        token["course_num"] = user.course_num
        token["must_change_password"] = user.must_change_password
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = MeSerializer(self.user).data
        return data


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenSerializer


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    auth_action = "token_refresh"


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    # client sends refresh token to blacklist
    refresh = request.data.get("refresh")
    if not refresh:
        return Response({"detail": "refresh token required"}, status=400)
    try:
        token = RefreshToken(refresh)
        token.blacklist()
    except Exception:
        return Response({"detail": "invalid token"}, status=400)
    return Response({"detail": "logged out"})


@api_view(["GET"])
def me_view(request):
    # allow even if must_change_password (so frontend can see flag)
    return Response(MeSerializer(request.user).data)
me_view.auth_action = "me"


@api_view(["POST"])
def change_password_view(request):
    ser = ChangePasswordSerializer(data=request.data)
    ser.is_valid(raise_exception=True)

    request.user.set_password(ser.validated_data["new_password"])
    request.user.must_change_password = False
    request.user.save(update_fields=["password", "must_change_password"])
    return Response({"detail": "password updated"})
change_password_view.auth_action = "change_password"


class CreateUserView(generics.CreateAPIView):
    """
    Hierarchy enforcement + auto-fill org fields.
    """
    serializer_class = CreateUserSerializer
    permission_classes = [CanCreateUsers, MustChangePasswordBlocker]

    def post(self, request, *args, **kwargs):
        creator = request.user

        requested_role = request.data.get("role")
        if not requested_role:
            return Response({"detail": "role is required"}, status=400)

        # Admin/staff can create anything, but your policy says:
        # Admin creates only BC. We'll enforce that here:
        if creator.is_superuser or creator.is_staff:
            if requested_role != UserRole.BATTALION_COMMANDER:
                return Response({"detail": "Admin/staff can only create Battalion Commander"}, status=403)

        # Non-admin hierarchy
        if not (creator.is_superuser or creator.is_staff):
            allowed = CAN_CREATE.get(creator.role, set())
            if requested_role not in allowed:
                return Response({"detail": f"{creator.role} cannot create {requested_role}"}, status=403)

        # Build payload with auto fields
        payload = dict(request.data)

        if requested_role == UserRole.PLATOON_COMMANDER:
            # BC creates PC: must provide platoon number
            if creator.role != UserRole.BATTALION_COMMANDER:
                return Response({"detail": "Only Battalion Commander can create Platoon Commanders"}, status=403)
            if "platoon" not in payload:
                return Response({"detail": "platoon is required for Platoon Commander"}, status=400)
            payload["battalion"] = creator.battalion
            payload["course_num"] = creator.course_num
            payload["team"] = None

        elif requested_role == UserRole.TEAM_COMMANDER:
            # PC creates TC: must provide team number
            if creator.role != UserRole.PLATOON_COMMANDER:
                return Response({"detail": "Only Platoon Commander can create Team Commanders"}, status=403)
            if "team" not in payload:
                return Response({"detail": "team is required for Team Commander"}, status=400)
            payload["battalion"] = creator.battalion
            payload["course_num"] = creator.course_num
            payload["platoon"] = creator.platoon

        elif requested_role == UserRole.CADET:
            # TC creates cadets: platoon/team are automatic from TC
            if creator.role != UserRole.TEAM_COMMANDER:
                return Response({"detail": "Only Team Commander can create Cadets"}, status=403)
            payload["battalion"] = creator.battalion
            payload["course_num"] = creator.course_num
            payload["platoon"] = creator.platoon
            payload["team"] = creator.team

        elif requested_role == UserRole.BATTALION_COMMANDER:
            # Only admin/staff creates BC (already enforced)
            pass

        ser = self.get_serializer(data=payload)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)


class BulkCreateUsersView(generics.GenericAPIView):
    """
    Bulk creation: send {"role": "...", "users": [ {full_name,email,rank,platoon/team?}, ... ]}
    Useful for "declare how many" flows.
    """
    permission_classes = [CanCreateUsers, MustChangePasswordBlocker]
    serializer_class = BulkCreateSerializer

    def post(self, request):
        role = request.data.get("role")
        if not role:
            return Response({"detail": "role is required"}, status=400)

        bulk = BulkCreateSerializer(data=request.data)
        bulk.is_valid(raise_exception=True)

        created = []
        errors = []

        for idx, u in enumerate(bulk.validated_data["users"]):
            single_payload = dict(u)
            single_payload["role"] = role

            # Reuse CreateUserView logic by calling serializer with autofill rules
            # We replicate the autofill rules here:
            creator = request.user

            if creator.is_superuser or creator.is_staff:
                if role != UserRole.BATTALION_COMMANDER:
                    errors.append({"index": idx, "detail": "Admin/staff can only create Battalion Commander"})
                    continue

            if not (creator.is_superuser or creator.is_staff):
                allowed = CAN_CREATE.get(creator.role, set())
                if role not in allowed:
                    errors.append({"index": idx, "detail": f"{creator.role} cannot create {role}"})
                    continue

            if role == UserRole.PLATOON_COMMANDER:
                if creator.role != UserRole.BATTALION_COMMANDER:
                    errors.append({"index": idx, "detail": "Only BC can create PC"})
                    continue
                if "platoon" not in single_payload:
                    errors.append({"index": idx, "detail": "platoon is required"})
                    continue
                single_payload["battalion"] = creator.battalion
                single_payload["course_num"] = creator.course_num
                single_payload["team"] = None

            elif role == UserRole.TEAM_COMMANDER:
                if creator.role != UserRole.PLATOON_COMMANDER:
                    errors.append({"index": idx, "detail": "Only PC can create TC"})
                    continue
                if "team" not in single_payload:
                    errors.append({"index": idx, "detail": "team is required"})
                    continue
                single_payload["battalion"] = creator.battalion
                single_payload["course_num"] = creator.course_num
                single_payload["platoon"] = creator.platoon

            elif role == UserRole.CADET:
                if creator.role != UserRole.TEAM_COMMANDER:
                    errors.append({"index": idx, "detail": "Only TC can create cadets"})
                    continue
                single_payload["battalion"] = creator.battalion
                single_payload["course_num"] = creator.course_num
                single_payload["platoon"] = creator.platoon
                single_payload["team"] = creator.team

            ser = CreateUserSerializer(data=single_payload)
            if not ser.is_valid():
                errors.append({"index": idx, "detail": ser.errors})
                continue
            ser.save()
            created.append(ser.data)

        return Response({"created": created, "errors": errors}, status=200)
