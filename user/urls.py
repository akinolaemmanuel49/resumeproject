from django.urls import path

from user.views import (
    UserChangeEmailAction,
    UserChangePasswordAction,
    UserCreateView,
    UserDeleteAction,
    UserEditProfileView,
    UserProfileView,
    UserSettingsView,
)


app_name = "user"

urlpatterns = [
    path("create/", UserCreateView.as_view(), name="create-user-view"),
    path("profile/edit/", UserEditProfileView.as_view(), name="edit-profile-view"),
    path("profile/", UserProfileView.as_view(), name="profile-view"),
    path("settings/", UserSettingsView.as_view(), name="settings-view"),
    path(
        "settings/change-email",
        UserChangeEmailAction.as_view(),
        name="change-email-action",
    ),
    path(
        "settings/change-password",
        UserChangePasswordAction.as_view(),
        name="change-password-action",
    ),
    path("delete/", UserDeleteAction.as_view(), name="delete-user-action"),
]
