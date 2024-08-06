from dj_rest_auth.serializers import LoginSerializer


class AuthLoginSerializer(LoginSerializer):
    email = None
