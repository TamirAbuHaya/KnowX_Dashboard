from django.urls import path
from .views import LoginView, RefreshView, logout_view, me_view, change_password_view, CreateUserView, BulkCreateUsersView

urlpatterns = [
    path("token/", LoginView.as_view(), name="token"),
    path("token/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("logout/", logout_view, name="logout"),
    path("me/", me_view, name="me"),
    path("change-password/", change_password_view, name="change_password"),

    path("users/", CreateUserView.as_view(), name="create_user"),
    path("users/bulk/", BulkCreateUsersView.as_view(), name="bulk_create_users"),
]
