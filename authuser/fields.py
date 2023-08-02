from django import forms
from settings.submodels.model_types import Types

class ListTextWidget(forms.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list_%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list_%s" class="state-fields">' % self._name
        data_list += '</datalist>'

        return (text_html + data_list)




def TypeFilter(type=''):
    try:
        container = []
        if type != '':
            data =  Types.objects.all().filter(type=type)
            for x in data:
                data = (x.type,x.name)
                container.append(data)
        return container
    except:
        pass


    