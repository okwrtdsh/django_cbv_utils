from django import forms

from .widgets import (
    CalendarCheckboxSelectMultiple,
    DatePickerWidget, DateTimePickerWidget,
    NumericIntegerWidget, NumericPositiveIntegerWidget,
    NumericWidget, TimePickerWidget)


class SetFromControlMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SetFromControlMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if not isinstance(self.fields[field].widget, (
                    forms.CheckboxInput, forms.RadioSelect,
                    CalendarCheckboxSelectMultiple)):
                self.fields[field].widget.attrs.update(
                    {'class': "form-control"})


class SetDateTimePickerMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SetDateTimePickerMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field].widget, (
                    DateTimePickerWidget,
                    DatePickerWidget,
                    TimePickerWidget)):
                continue
            if isinstance(self.fields[field].widget, forms.DateTimeInput):
                self.fields[field].widget = DateTimePickerWidget()
            elif isinstance(self.fields[field].widget, forms.DateInput):
                self.fields[field].widget = DatePickerWidget()
            elif isinstance(self.fields[field].widget, forms.TimeInput):
                self.fields[field].widget = TimePickerWidget()


class SetPositiveIntegerMixin(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SetPositiveIntegerMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field].widget, (
                    NumericWidget,
                    NumericIntegerWidget,
                    NumericPositiveIntegerWidget)):
                continue
            if isinstance(self.fields[field].widget, forms.NumberInput):
                self.fields[field].widget = NumericPositiveIntegerWidget()
