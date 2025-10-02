from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.models import User


# def shorter_permissions(permission_set):
#
#     for perm in permission_set:
#         if perm.startswith('community.') or perm.startswith('buckets.'):
#             parts = perm.split('.')
#             domain = parts[0][0]
#             [verb, noun] = parts[1].split('_')
#             # shorten verbs to their first letter, nouns stay as are
#             if verb in ['change', 'view', 'delete', 'add']:
#                 verb = verb[0]
#
#             yield domain + '.' + verb + '_' + noun


class MvTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get default token
        token = super().get_token(user)

        # user.get_all_permissions()

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        # token['permissions'] = list(user.get_all_permissions())
        token['permission_ids'] = [perm['id'] for perm in user.user_permissions.values('id')]

        # You can add any field from your user model
        return token

# class MvTokenRefreshSerializer(TokenRefreshSerializer):
#
#     @classmethod
#     def get_token(cls):
#         pass