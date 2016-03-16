from django import forms
from django_cbv_utils.forms import SearchForm
from example.models import MyModel

class MyModelSearchForm(SearchForm):
    queryset_filter = {
        "name": {"op": "icontains_or", "flds": ["name_icontains_or"]},
        "created": {"op": "date", "flds": ["created_date"]},
        "birthday": {"op": "gte_lte", "flds": [
            "birthday_start", "birthday_end"]},
        "number": {"op": "gt_lt", "flds": [
            "number_gt", "number_lt"]},
        "status": {"flds": ["status"]},
    }
    queryset_exclude = {
        "name": {"op": "icontains_and", "flds": ["exclude_name_icontains_and"]},
    }
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
    exclude_name_icontains_and = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(MyModelSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control"})

