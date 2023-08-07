from django import template
from django.core import serializers
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def nav_tags(host='', opts=None, classname='', site='admin'):

    links = ''
    
    if opts:
        link_paths = str(opts).split('.')
        link_paths2 = link_paths[0] # count from the back -1
        
        for x in range(0, len(link_paths)):
            index = x-1
            if index != 0:
                # /{site}/{link_paths2}
                links += f"<li class='{classname}'> <a  href='#'>{link_paths2}</a></li><li class='{classname}'><a href='/{site}/{link_paths[x]}/{link_paths[index]}'>{link_paths[index]}</a></li>"
        
        return format_html(links)
    
    return ''
    
