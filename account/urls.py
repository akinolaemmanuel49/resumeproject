from django.urls import path

from account.views import (
    AccountChangeEmailAction,
    AccountChangePasswordAction,
    AccountCreateView,
    AccountDeleteAction,
    AccountDummyView,
    AccountEditProfileView,
    AccountLoginView,
    AccountLogoutView,
    AccountProfileView,
    AccountSettingsView,
)

urlpatterns = [
    path("dummy/", AccountDummyView.as_view(), name="dummy-view"),
    path(
        "settings/change-password",
        AccountChangePasswordAction.as_view(),
        name="change-password-action",
    ),
    path(
        "settings/change-email",
        AccountChangeEmailAction.as_view(),
        name="change-email-action",
    ),
    path("delete/", AccountDeleteAction.as_view(), name="delete-account-action"),
    path("settings/", AccountSettingsView.as_view(), name="settings-view"),
    path("profile/", AccountProfileView.as_view(), name="profile-view"),
    path("profile/edit", AccountEditProfileView.as_view(), name="edit-profile-view"),
    path("create/", AccountCreateView.as_view(), name="account-create-view"),
    path("login/", AccountLoginView.as_view(), name="login-view"),
    path("logout/", AccountLogoutView.as_view(), name="logout-view"),
]
