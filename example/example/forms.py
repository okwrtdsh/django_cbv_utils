from django import forms
from django_cbv_utils.forms import SearchForm
from example.models import MyModel

class MyModelSearchForm(SearchForm):
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
    exclude_name_icontains_and = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(MyModelSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})

