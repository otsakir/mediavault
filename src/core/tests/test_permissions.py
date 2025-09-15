from enum import Enum
from core.security import PermissionSchemeBase


class MyPermissionScheme(PermissionSchemeBase):

    class Permissions(Enum):
        Read = 0
        Write = 1
        Execute = 2

        List = 4

    def asdf(self, a: Permissions):
        pass


def test_single_permission():

    p = MyPermissionScheme('TF..T')
    assert p.allows(p.Permissions.Read)
    assert not p.allows(p.Permissions.Write)
    assert not p.allows(p.Permissions.Execute)
    assert p.allows(p.Permissions.List)


def test_elliptic_permission():

    p = MyPermissionScheme('TF')
    assert not p.allows(p.Permissions.Execute)


def test_many_permissions():
    p = MyPermissionScheme('TFFFT')
    assert p.allows_all([p.Permissions.Read, p.Permissions.List])

def test_permissions_as_strings():
    p = MyPermissionScheme('TFFFT')
    permission_strings = p.allowed_permissions()
    assert 'Read' in permission_strings
    assert 'Write' not in permission_strings

def test_to_permissions_string():

    permissions_string = MyPermissionScheme.to_permissions_string([MyPermissionScheme.Permissions.Read, MyPermissionScheme.Permissions.Write])
    assert permissions_string == 'TT...'


