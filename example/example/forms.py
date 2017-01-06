from django import forms

from django_cbv_utils.forms import (
    DateTimePickerMixin, FormControlMixin, PositiveIntegerMixin, SearchForm,
)
from django_cbv_utils.forms.widgets import (
    BootstrapFileInputWidget, DatePickerWidget, DateTimePickerWidget,
    NumericIntegerWidget, NumericPositiveIntegerWidget, NumericWidget,
    TimePickerWidget,
)
from example.models import MyModel


class MyModelSearchForm(
        SearchForm, FormControlMixin,
        DateTimePickerMixin, PositiveIntegerMixin):
    queryset_filter = [
        {"targets": "name", "op": "icontains_or",
         "fields": "name_icontains_or"},
        {"targets": "created", "op": "date", "fields": "created_date"},
        {"targets": "birthday", "op": "gte_lte",
         "fields": ["birthday_start", "birthday_end"]},
        {"targets": "number", "op": "gt_lt",
         "fields": ["number_gt", "number_lt"]},
        {"targets": "status", "fields": "status"},
        {"targets": ["name", "name2"],
         "op": "icontains_or", "fields": "name_or_name2"},
        {"targets": ["id", "number"],
         "op": "or", "fields": "id_or_number"},
    ]
    queryset_exclude = [
        {"targets": "name", "op": "icontains_and",
         "fields": "exclude_name_icontains_and"}
    ]

    class Meta:
        model = MyModel
        fields = ["status"]

    name_icontains_or = forms.CharField()
    created_date = forms.DateField()
    birthday_start = forms.DateField()
    birthday_end = forms.DateField()
    number_gt = forms.IntegerField()
    number_lt = forms.IntegerField()
    status = forms.TypedChoiceField(
        choices=[("", "-----")] + list(MyModel.STATUS_CHOICES),
        coerce=int,
        empty_value=None
    )
    name_or_name2 = forms.CharField()
    id_or_number = forms.IntegerField()
    exclude_name_icontains_and = forms.CharField()
    datetime_picker = forms.DateTimeField(widget=DateTimePickerWidget())
    datetime_picker2 = forms.DateTimeField(widget=DateTimePickerWidget(
        options={
            "toolbarPlacement": "top",
            "showClear": True,
            "showClose": True,
            "sideBySide": False,
        }))
    date_picker = forms.DateField(widget=DatePickerWidget(
        options={
            "showTodayButton": True,
            "viewMode": "decades",
        }))
    date_picker2 = forms.DateField(widget=DatePickerWidget(
        options={
            "viewMode": "years",
            "format": "YYYY-MM",
            "glyphicon": "glyphicon-calendar",
        }))
    time_picker = forms.TimeField(widget=TimePickerWidget())
    time_picker2 = forms.TimeField(widget=TimePickerWidget(
        options={
            "format": "HH:mm:SS",
            "stepping": 30,
        }))
    numerc = forms.IntegerField(widget=NumericWidget())
    numeric_integer = forms.IntegerField(widget=NumericIntegerWidget())
    numeric_positive_integer = forms.IntegerField(
        widget=NumericPositiveIntegerWidget())
    bootstrap_filewidget = forms.FileField(widget=BootstrapFileInputWidget())
