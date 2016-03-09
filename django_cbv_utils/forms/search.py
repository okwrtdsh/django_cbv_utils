from django.forms import ModelForm

class SearchForm(ModelForm):
    queryset_filter = {}
    queryset_exclude = {}

    class Meta:
        model = None
        fields = [
        ]

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False
