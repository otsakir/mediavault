from django import template
from django.utils.safestring import mark_safe

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


@register.simple_tag
def icon(icon_name, class_name=None):
    icons = {
        'trash': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>',
        'folder-plus': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 10.5v6m3-3H9m4.06-7.19-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" /></svg>',
        'arrow-uturn-left': '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6"><path stroke-linecap="round" stroke-linejoin="round" d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" /></svg>'
    }

    if icon_name in icons:
        return mark_safe(icons[icon_name].format(class_name=class_name))
    else:
        return ''




