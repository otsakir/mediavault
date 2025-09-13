from typing import Iterable


class PermissionSchemeBase:

    last_permission_index = None
    data = None

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
        for perm in self.Permissions:
            i = perm.value
            perm_char = perm_string[i] if i < len(perm_string) else '.'
            self.data[i] = True if perm_char == 'T' else False

    def allows(self, perm):
        return self.data[perm.value]

    def allows_all(self, iterable: Iterable):
        return all(self.allows(p) for p in iterable)

    @classmethod
    def length(cls):
        return cls.last_permission_index+1
