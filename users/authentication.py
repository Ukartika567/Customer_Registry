from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken

#User JWT Authentication and get access token from refresh token internally without call api/refresh/ api
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            return None  # No token found, let DRF handle it

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            access_token = AccessToken(raw_token)
            # Check if token is expired
            if access_token["exp"] < make_aware(datetime.utcnow()).timestamp():
                return self.refresh_token(request)  # Auto-refresh if expired
            return self.get_user(validated_token=access_token), access_token

        except Exception:
            return self.refresh_token(request)  # Try refreshing if token is invalid

    def refresh_token(self, request):
        old_refresh_token = request.COOKIES.get("refresh_token")
        if not old_refresh_token:
            raise AuthenticationFailed("Authentication failed, please log in again.")

        try:
            old_refresh = RefreshToken(old_refresh_token)

            # Blacklist the old refresh token
            try:
                BlacklistedToken.objects.create(token=old_refresh)
            except Exception:
                pass  # Ignore if already blacklisted

            # Generate new tokens
            new_refresh = RefreshToken.for_user(self.get_user(validated_token=old_refresh))
            new_access_token = str(new_refresh.access_token)

            response = JsonResponse({"detail": "Tokens refreshed successfully"})

            # Set new HttpOnly cookies
            response.set_cookie(
                "refresh_token",
                str(new_refresh),
                httponly=True,
                samesite="Strict",
                secure=True,
                path="/",
            )
            response.set_cookie(
                "access_token",
                str(new_access_token),
                httponly=True,
                samesite="Strict",
                secure=True,
                path="/"
            )

            return self.get_user(validated_token=new_refresh.access_token), new_refresh.access_token

        except Exception:
            raise AuthenticationFailed("Invalid refresh token, please log in again.")

##Read token from cookie for passing in header with Bearer iternally
class JWTAuthenticationFromCookie(JWTAuthentication):
    def authenticate(self, request):
        # Look for access token in cookie
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
