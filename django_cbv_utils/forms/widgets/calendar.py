import calendar
import datetime
from collections import defaultdict
from itertools import chain

from django.forms.utils import flatatt
from django.forms.widgets import SelectMultiple, SubWidget
from django.utils.datastructures import MergeDict, MultiValueDict
from django.utils.encoding import (force_str, force_text,
                                   python_2_unicode_compatible, smart_text)
from django.utils.html import format_html, html_safe
from django.utils.safestring import mark_safe


@html_safe
@python_2_unicode_compatible
class CalendarCheckboxInput(SubWidget):
    input_type = 'checkbox'

    def __init__(self, name, value, attrs, choice_value, date, date_format):
        self.name = name
        self._value = value
        self.attrs = attrs
        self.choice_value = force_text(choice_value)
        self.date = date
        self.date_format = date_format
        self.value = self.to_split(value)
        if 'id' in self.attrs:
            self.attrs['id'] += "_%s" % self.get_value()
        self.value = dict((force_text(i), set(v)) for i, v in self.value)

    def __str__(self):
        return self.render()

    def to_split(self, value):
        d = defaultdict(lambda: [])
        for val in value:
            val = smart_text(val)
            k, v = val.split('-', 1)
            d[k].append(self.to_date(v))
        return list(d.items())

    def to_date(self, value):
        return datetime.datetime.strptime(
            force_str(value),
            self.date_format).date()

    def is_checked(self):
        return self.date in self.value.get(self.choice_value, [])

    def get_value(self):
        return "{0}-{1}".format(self.choice_value,
                                self.date.strftime(self.date_format))

    def tag(self, attrs=None):
        attrs = attrs or self.attrs
        final_attrs = dict(
            attrs, type=self.input_type, name=self.name,
            value=self.get_value())
        if self.is_checked():
            final_attrs['checked'] = 'checked'
        if final_attrs.get("class"):
            final_attrs["class"] += " day%s" % self.date.day
        else:
            final_attrs["class"] = "day%s" % self.date.day
        return format_html('<input{} />', flatatt(final_attrs))

    def render(self, name=None, value=None, attrs=None, choices=()):
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        return format_html('{}', self.tag(attrs))


class CalendarRadioInput(CalendarCheckboxInput):
    input_type = 'radio'

    def __init__(self, name, value, attrs, choice_value, date, date_format):
        super().__init__(name, value, attrs, choice_value, date, date_format)
        self.name += self.date.strftime("%d")


@html_safe
@python_2_unicode_compatible
class CalendarCheckboxRenderer(object):
    choice_input_class = CalendarCheckboxInput
    tr_html = '<tr>{label}{content}</tr>'
    label_html = '<td colspan="4">{choice_label}</td>'
    td_html = '<td class="{status}">{subwidget}</td>'

    def __init__(self, name, value, attrs, choices, disables,
                 year, month, date_format, *args, **kwargs):
        self.name = name
        self.value = value
        self.attrs = attrs
        self.choices = choices
        self.year = year
        self.month = month
        self.date_format = date_format
        self.days = calendar.monthrange(self.year, self.month)[1]
        self.disables = dict((force_text(i), set(v))
                             for i, v in disables)

    def __str__(self):
        return self.render()

    def is_vacant(self, choice_value, date):
        return date not in self.disables.get(
            force_text(choice_value), [])

    def render(self):
        output = ['<tbody>']
        for choice in self.choices:
            output_tr = []
            choice_value, choice_label = choice
            for i in range(self.days):
                date = datetime.date(self.year, self.month, i+1)
                if self.is_vacant(choice_value, date):
                    attrs = self.attrs.copy()
                    w = self.choice_input_class(
                        self.name, self.value, attrs,
                        choice_value, date, self.date_format)
                    output_tr.append(format_html(
                        self.td_html,
                        status="vacant",
                        subwidget=force_text(w)))
                else:
                    output_tr.append(format_html(
                        self.td_html,
                        status="occupied",
                        subwidget=''))
            output.append(format_html(
                self.tr_html,
                content=mark_safe('\n'.join(output_tr)),
                label=format_html(self.label_html, choice_label=choice_label)
            ))
        output.append('</tbody>')
        return mark_safe('\n'.join(output))


class CalendarRadioRenderer(CalendarCheckboxRenderer):
    choice_input_class = CalendarRadioInput


class CalendarCheckboxSelectMultiple(SelectMultiple):
    _empty_value = []
    renderer = CalendarCheckboxRenderer
    LABEL_NAME = "部屋"
    LABEL_ALL = "全室"
    LABEL_DATE = "日付"
    LABEL_WEEKDAY = "曜日"
    style_attr = "table-layout: fixed;"
    class_attrs = ["calendar", "table", "table-bordered",  "table-hover"]

    def __init__(self, attrs=None, choices=(), disables=()):
        super().__init__(attrs, choices)
        self.disables = list(disables)

    def get_renderer(self, name, value, attrs=None, choices=(),
                     disables=(), year=None, month=None,
                     date_format=None, *args, **kwargs):
        if value is None:
            value = self._empty_value
        final_attrs = self.build_attrs(attrs)
        choices = list(chain(self.choices, choices))
        disables = list(chain(self.disables, disables))
        return self.renderer(name, value, final_attrs, choices, disables,
                             year, month, date_format, *args, **kwargs)

    def render(self, name, value, attrs=None, choices=(), disables=()):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        self.first_weekday, self.days = calendar.monthrange(
            self.year, self.month)
        final_attrs["style"] = self.style_attr
        final_attrs["class"] = " ".join(self.class_attrs)
        output = [format_html('<table{}>', flatatt(final_attrs))]
        thead = self.render_thead()
        output.append(thead)
        tbody = self.get_renderer(
            name, value, attrs, choices, disables,
            self.year, self.month, self.date_format).render()
        if tbody:
            output.append(tbody)
        output.append(thead)
        output.append('</table>')
        return mark_safe('\n'.join(output))

    def render_thead(self):
        output = ['<thead><tr class="days">']
        output.append('<th colspan="2" rowspan="2">{}</th>'.format(
            self.LABEL_NAME))
        output.append('<th colspan="2">{}</th>'.format(self.LABEL_DATE))
        output.extend('<th>{}</th>'.format(i + 1) for i in range(self.days))
        output.append('</tr><tr class="wdays">')
        output.append('<th colspan="2">{}</th>'.format(self.LABEL_WEEKDAY))
        for i in range(self.days):
            weekday = (self.first_weekday + i) % 7
            output.append('<th class="wday{0}">{1}</th>'.format(
                weekday,
                self.day_abbr[weekday]
            ))
        output.append('</tr></thead>')
        return mark_safe(''.join(output))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)


class CalendarRadioSelectMultiple(CalendarCheckboxSelectMultiple):
    renderer = CalendarRadioRenderer

    def value_from_datadict(self, data, files, name):
        days = calendar.monthrange(self.year, self.month)[1]
        if isinstance(data, (MultiValueDict, MergeDict)):
            values = []
            for i in range(days):
                value = data.get("%s%02d" % (name, i+1))
                if value:
                    values.append(value)
            return values
        return data.get(name, None)
