from django import template

register = template.Library()


def field_type(field):
    try:
        t = field.widget.__class__.__name__
        return t
    except Exception as e:
        print(f'Exception in field_type filter: {e}')
        return ''


classes_for_tag = {
    'button': 'hover:bg-red-500 text-white px-4 p-2 bg-black rounded-md',
    'select': 'hover:bg-red-500 px-4 p-2 rounded-md',
    'check': 'hover:bg-red-500 px-4 p-2 rounded-md',
    'textarea': 'border border-slate-500 rounded p-2 w-full',
    'text': 'shadow appearance-none border border-slate-500 rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
    'link': 'hover:underline',
}


def append_class(classes_str, tag ):
    more_classes = classes_for_tag.get(tag, '')
    return f'{classes_str} {more_classes}'


register.filter('field_type', field_type)
register.filter('append_class', append_class)

