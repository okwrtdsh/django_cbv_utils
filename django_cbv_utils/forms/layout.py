from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .widgets import DateTimePickerWidget, DatePickerWidget,\
     TimePickerWidget


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


class SetFromControlMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SetFromControlMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if not isinstance(self.fields[field].widget,
                              (forms.CheckboxInput, forms.RadioSelect)):
                self.fields[field].widget.attrs.update(
                    {'class': "form-control"})


class SetDateTimePicerMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SetDateTimePicerMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field].widget, (
                    DateTimePickerWidget,
                    DatePickerWidget,
                    TimePickerWidget,)):
                continue
            if isinstance(self.fields[field].widget, forms.DateTimeInput):
                self.fields[field].widget = DateTimePickerWidget()
            elif isinstance(self.fields[field].widget, forms.DateInput):
                self.fields[field].widget = DatePickerWidget()
            elif isinstance(self.fields[field].widget, forms.TimeInput):
                self.fields[field].widget = TimePickerWidget()

