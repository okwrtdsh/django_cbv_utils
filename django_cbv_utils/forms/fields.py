import calendar
import copy
import datetime
from collections import defaultdict

from django.core.exceptions import ValidationError
from django.forms import MultipleChoiceField
from django.forms.fields import CallableChoiceIterator
from django.utils import timezone
from django.utils.encoding import force_str, force_text, smart_text

from .widgets.calendar import CalendarCheckboxSelectMultiple


class CalendarMultipleChoiceField(MultipleChoiceField):
    """
    choices = ((value1, label1), ...)
    disables = (
        (value1: [date1, ...]),
        ...
    )
    """
    widget = CalendarCheckboxSelectMultiple

    def __init__(self, choices=(), required=True, widget=None,
                 label=None, initial=None, help_text='',
                 year=None, month=None, disables=(),
                 date_format=None, day_abbr=None, *args, **kwargs):
        super().__init__(required=required, widget=widget, label=label,
                         initial=initial, help_text=help_text, *args, **kwargs)
        self.choices = choices
        if year is None:
            year = timezone.now().year
        if month is None:
            month = timezone.now().month
        self.year = year
        self.month = month
        self.disables = disables
        if date_format is not None:
            self.date_format = date_format
        else:
            self.date_format = '%Y%m%d'
        if day_abbr is not None:
            self.day_abbr = day_abbr
        else:
            self.day_abbr = calendar.day_abbr

    def __deepcopy__(self, memo):
        result = super().__deepcopy__(memo)
        result._disables = copy.deepcopy(self._disables, memo)
        result._day_abbr = copy.deepcopy(self._day_abbr, memo)
        return result

    def _get_disables(self):
        return self._disables

    def _set_disables(self, value):
        if callable(value):
            value = CallableChoiceIterator(value)
        else:
            value = list(value)
        self._disables = self.widget.disables = value

    disables = property(_get_disables, _set_disables)

    def _get_year(self):
        return self._year

    def _set_year(self, value):
        if callable(value):
            value = value()
        else:
            value = int(value)
        self._year = self.widget.year = value

    year = property(_get_year, _set_year)

    def _get_month(self):
        return self._month

    def _set_month(self, value):
        if callable(value):
            value = value()
        else:
            value = int(value)
        self._month = self.widget.month = value

    month = property(_get_month, _set_month)

    def _get_date_format(self):
        return self._date_format

    def _set_date_format(self, value):
        if callable(value):
            value = value()
        else:
            value = value
        self._date_format = self.widget.date_format = value

    date_format = property(_get_date_format, _set_date_format)

    def _get_day_abbr(self):
        return self._day_abbr

    def _set_day_abbr(self, value):
        if callable(value):
            value = value()
        else:
            value = list(value)
        self._day_abbr = self.widget.day_abbr = value

    day_abbr = property(_get_day_abbr, _set_day_abbr)

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages[
                                  'invalid_list'], code='invalid_list')
        d = defaultdict(lambda: [])
        for val in value:
            val = smart_text(val)
            if '-' not in val:
                raise ValidationError(self.error_messages[
                                      'invalid'], code='invalid')
            k, v = val.split('-', 1)
            d[k].append(self.to_date(v))
        return list(d.items())

    def to_date(self, value):
        if isinstance(value, str):
            try:
                return self.strptime(value, self.date_format)
            except (ValueError, TypeError):
                pass
        raise ValidationError(self.error_messages['invalid'], code='invalid')

    def strptime(self, value, format):
        return datetime.datetime.strptime(force_str(value), format).date()

    def validate(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages[
                                  'required'], code='required')
        # Validate that each value in the value list is in self.choices.
        for val in value:
            if not self.valid_value(val):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )

    def valid_value(self, value):
        """
        Check to see if the provided value is a valid choice
        """
        text_value = force_text(value[0])
        date_list = value[1]
        disables_date = dict((force_text(i), set(v)) for i, v in self.disables)
        # Check date
        for date in date_list:
            if date.year != self.year:
                return False
            if date.month != self.month:
                return False
            if disables_date.get(text_value):
                if date in disables_date[text_value]:
                    return False
        # Check value
        for k, v in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == k2 or text_value == force_text(k2):
                        return True
            else:
                if value == k or text_value == force_text(k):
                    return True
        return False

    def has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = dict((force_text(i), set(v)) for i, v in initial)
        data_set = dict((force_text(i), set(v)) for i, v in data)
        return data_set != initial_set
