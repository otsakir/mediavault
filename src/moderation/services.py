from core.models import Community, Member
from django.contrib.auth.models import User
from exceptions import AlreadyMemberException
from django.db import transaction


class CommunityService:

    @staticmethod
    @transaction.atomic
    def create_community(owner: User, name: str):

        members = Member.objects.filter(user=owner)
        if len(members) > 0:
            raise AlreadyMemberException()

        community = Community(name)
        community.save()
        membership = Member(community=community, user=owner)
        membership.save()

        return community

    # @staticmethod
    # def in_community():
