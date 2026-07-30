from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError


User = get_user_model()


def login_user(login: str, password: str):

    user = User.objects.filter(
        Q(username__iexact=login) |
        Q(email__iexact=login)
    ).first()

    if not user:
        raise AuthenticationFailed("Invalid username/email or password.")

    authenticated_user = authenticate(
        username=user.username,
        password=password,
    )

    if not authenticated_user:
        raise AuthenticationFailed("Invalid username/email or password.")

    refresh = RefreshToken.for_user(authenticated_user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": authenticated_user,
    }


def logout_user(refresh_token: str):

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

    except Exception:
        raise ValidationError(
            {"refresh": ["Invalid or expired refresh token."]}
        )