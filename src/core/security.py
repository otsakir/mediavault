import re


class PermissionScheme:
    """A base class for defining custom permissions"""

    max_count = 30
    """Maximum number of permission definitions allowed"""

    data = '.' * max_count
    validation_exp = re.compile('^[TF\.]*$')  # only T, F, '.' characters allowed
    valid_characters = ['T', 'F', '.']

    """Determine what will be returned when running, for example, perm.read()"""
    def resolve_value_at_index(self, index, default_value) -> bool:
        at_index = self.data[index]
        if at_index == '.':
            at_index = default_value
        return at_index == 'T'

    def generate_getter(self, name, index, default_value):
        def f():
            # print("inside getter for", name, 'at position', index, ', data: ', self.data)
            return self.resolve_value_at_index(index, default_value)
        return f

    def validate_permission_char(self, char):
        if char not in self.valid_characters:
            raise ValueError(f'invalid permission character {char}. Accepted values {self.valid_characters}')

    def __init__(self, permission_string):
        if len(permission_string) > self.max_count or not self.validation_exp.match(permission_string):
            raise ValueError(f'invalid permission string: {permission_string}')
        self.data = permission_string + self.data[len(permission_string):] # overwrite default 'data' with given permission string but keep the end of it

        permission_fields = [i for i in self.__class__.__dict__.items() if not i[0].startswith('__')]

        i = 0
        for field_name, field_value in permission_fields:
            self.validate_permission_char(field_value)
            self.__setattr__(field_name, self.generate_getter(field_name, i, field_value))
            i = i + 1
