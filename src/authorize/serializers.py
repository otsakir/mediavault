from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MvTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get default token
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["is_staff"] = user.is_staff


        # You can add any field from your user model
        return token