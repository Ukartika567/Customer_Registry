from django.utils.deprecation import MiddlewareMixin

#Internally passes token in each API request, in credentials:True parameter , 
# Dosen't need  a /token/refresh/ API call for get access token from refresh token.
# cookie is HttpOnly secure so 
class TokenFromCookieMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if "access_token" is in cookies
        access_token = request.COOKIES.get("access_token")

        if access_token:
            # Set "Authorization" header dynamically
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
