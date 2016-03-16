from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms


class SimpleLayoutMixin(forms.BaseForm):

    def __init__(self, *args, **kwargs):
        super(SimpleLayoutMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})
        self.helper = FormHelper()
        field_list = list(self.fields)
        field_list = self.add_fields(field_list)
        self.helper.layout = Layout(*field_list)

    def add_fields(self, field_list):
        return field_list


class SubmitLayoutMixin(SimpleLayoutMixin):

    def add_fields(self, field_list):
        field_list.append(Submit('submit', '送信'))
        return field_list

