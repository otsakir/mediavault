from typing import Iterable


class PermissionSchemeBase:

    last_permission_index = None
    data = None
    permissions_as_strings = []  # an array with all permissions that are set

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.last_permission_index = max(permission.value for permission in cls.Permissions)

    def __init__(self, perm_string):
        """
        Populates the internal permission data array using the given permission string. Checks only indexes defined
        in nested Permission class. Sets permission to True only if there is letter 'T' in the respective
        permission_string index.

        Args:
            perm_string (str): a permission string like 'TFF.F.TF"

        Throws:

        """

        self.data = [False]*(self.last_permission_index+1)  # so make sure data[] has available slots for all indexes defined in the Permission enum.
        self.permissions_as_strings.clear()
        for perm in self.Permissions:
            i = perm.value
            perm_char = perm_string[i] if i < len(perm_string) else '.'
            if perm_char == 'T':
                self.data[i] = True
                self.permissions_as_strings.append(perm.name)
            else:
                self.data[i] = False


    def allows(self, perm):
        return self.data[perm.value]

    def allows_all(self, iterable: Iterable):
        return all(self.allows(p) for p in iterable)

    @classmethod
    def length(cls):
        return cls.last_permission_index+1

    def allowed_permissions(self):
        return self.permissions_as_strings

    @classmethod
    def to_permissions_string(cls, perm_list: list):
        char_list = ['.']*(cls.last_permission_index+1)
        for perm in cls.Permissions:
            if perm in perm_list:
                char_list[perm.value] = 'T'

        permissions_string = ''.join(char_list)
        return permissions_string




