from django import template
from django.core import serializers
from django.utils.html import format_html
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from operator import methodcaller

register = template.Library()

def table_head(object, **kwargs):
    heads =  object.list_display
    table = ""
    table += "<thead>"
    table += "<tr>"
    clss = 'text-uppercase text-secondary text-xxs font-weight-bolder opacity-7'
    # table += f"<th data-sortable='true' style='width: 9.25925925925926%'>#</th>"
    # table += f"<th class='{clss}'  data-sortable='false' style='width: 9.25925925925926%'><input type='checkbox'  name='delete_checkbox_main' class='delete_checkbox_main'  id='delete_checkbox_main' /></th>"
    for head in heads:
        table += f"<th class='{clss}' data-sortable='true' style='width: 9.25925925925926%'>{str(head).replace('_', ' ').upper()}</th>"
    table += f"<th class='{clss}' data-sortable='true' style='width: 9.25925925925926%'>Remove</th>"
    table += "</tr>"
    table += "</thead>"
    return table


def table_body(object=None, request=None):
    try:
        # print(object.model_admin.trackFunction)
        heads =  object.list_display
        list_display_links =  object.list_display_links
        table = ""
       
        counter = 0
        index_counter =  1
        table += "<tbody>"
        for tbody in object.result_list:
            pk = eval("tbody.pk")
            table += f"<tr data-index='{counter}'>"
            # table += f"<td>{index_counter}</td>"
            # table += f"<td><input type='checkbox' name='delete_checkbox' value='{pk}' class='delete_checkbox'  id='delete_checkbox_{index_counter}' /></td>"
            for head in heads:
                table += f"<td>"
                # print(hasattr(eval(f"object.model"), head), head)
                # include a function call from either model or admin
                if hasattr(object.model, head) and callable(getattr(object.model, head)):
                   
                    # this will check if the attribute of the class is callable
                    method = getattr(object.model, head)
                    data = methodcaller(method.__name__)(tbody)  # Call the method with 'tbody' as the 'self' argument
                    table += f"{data}"
                
                else: 
                    if head in list_display_links:
                    # check if it is a function
                        data = eval(f"tbody.{head}")
                        table += f"<a href='{pk}/change' class=''> {data}  </a>"
                    else: 
                        data = eval(f"tbody.{head}")
                        table += f"{data}"
                    table += "</td>"
            table += f"<td><a href='{tbody.pk}/delete' class='link' >Delete</a></td>"
            table += "</tr>"
            counter += 1
            index_counter += 1
        table += "</tbody>"
        return table
    
    except Exception as e:
        return str(e)


@register.simple_tag
def change_list_tag(object=None, request=None):

    table = ""
    if object == None:
        return None
    table +=  table_head(object=object)
    table +=  table_body(object=object, request=request)

    return format_html(table)


@register.simple_tag
def user_profile(object=None, fields=''):
    try:
        fields =  fields.split(',')
        table = ""
        if object:
            for key in fields:
                data = eval(f"object.{key}")
                table += "<tr>"
                table += f"<td>{str(key).replace('_', ' ').upper()}: </td>"
                table += f"<td>{data}</td>"
                table += "</tr>"
            return format_html(table)
        return ''
    except Exception as e:
        return str(e)