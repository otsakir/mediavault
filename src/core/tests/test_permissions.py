from core.security import PermissionScheme
import pytest


class PermissionSchemeA(PermissionScheme):
    read = '.'
    write = '.'
    delete = '.'
    list = 'T'


def test_permissions():
    perm_scheme = PermissionSchemeA('TF.....')
    assert perm_scheme.read() is True
    assert perm_scheme.write() is False
    assert perm_scheme.delete() is False
    assert perm_scheme.list() is True

    # assert too long permission strings fail
    with pytest.raises(ValueError):
        PermissionScheme('.'*31)

    with pytest.raises(ValueError):
        perm_scheme = PermissionScheme('ASDF')




