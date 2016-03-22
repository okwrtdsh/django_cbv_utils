import re
import datetime
from django.db.models import Q
from django.forms import ModelForm

class SearchForm(ModelForm):
    queryset_filter = []
    queryset_exclude = []

    custom_lookup = [
        'or',
        'date',
        'gt_lt',
        'gt_lte',
        'gte_lt',
        'gte_lte',
        'icontains_or',
        'icontains_and',
    ]

    class Meta:
        model = None
        fields = []

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def get_queryset(self, queryset):
        if not self.is_valid():
            return queryset

        queries = Q()
        queries &= self._get_queries(self.queryset_filter)
        queries &= ~self._get_queries(self.queryset_exclude)
        return queryset.filter(queries).distinct()

    def _get_queries(self, queryset_filter):
        queries = Q()
        for filter_dict in queryset_filter:
            operator = filter_dict.get('op', '')

            if isinstance(filter_dict['targets'], (tuple, list)):
                target_list = filter_dict['targets']
            else:
                target_list = [filter_dict['targets']]

            if isinstance(filter_dict['fields'], (tuple, list)):
                if len(filter_dict['fields']) > 1:
                    data = []
                    for field in filter_dict['fields']:
                        data.append(self.cleaned_data[field])
                else:
                    data = self.cleaned_data[filter_dict['fields'][0]]
                    if data is None:
                        continue
            else:
                data = self.cleaned_data[filter_dict['fields']]
                if data is None:
                    continue

            if not operator:
                q = Q()
                for target in target_list:
                    q |= Q(**{target: data})
                queries &= q
                continue

            if operator not in self.custom_lookup:
                q = Q()
                for target in target_list:
                    q |= Q(**{'{0}__{1}'.format(
                        target, operator): data})
                queries &= q
                continue

            if operator == 'or':
                q = Q()
                for target in target_list:
                    if data is not None:
                        q |= Q(**{target: data})
                queries &= q
                continue

            if operator == 'date':
                if not isinstance(data, datetime.date):
                    continue
                q = Q()
                for target in target_list:
                    q |= Q(**{'{0}__{1}'.format(target, attr): getattr(
                        data, attr) for attr in ("year", "month", "day")})
                queries &= q
                continue

            if operator in ('gt_lt', 'gt_lte', 'gte_lt', 'gte_lte'):
                q = Q()
                for target in target_list:
                    _q = Q()
                    for i, v in enumerate(data):
                        if v is not None:
                            _q &= Q(**{'{0}__{1}'.format(
                                target, operator.split("_")[i]): v})
                    q |= _q
                queries &= q
                continue

            if operator == "icontains_or":
                if not isinstance(data, str) or not data:
                    continue
                q = Q()
                for target in target_list:
                    for v in re.split("\s", data):
                        q |= Q(**{'{0}__icontains'.format(target): v})
                queries &= q
                continue

            if operator == "icontains_and":
                if not isinstance(data, str) or not data:
                    continue
                q = Q()
                for target in target_list:
                    q |= Q(**{'{0}__icontains'.format(target): v
                        for v in re.split("\s", data)})
                queries &= q
                continue

            queries = self.get_queries(
                queries, filter_dict, target_list, operator, data)

        return queries

    def get_queries(self, queries, filter_dict, target_list, operator, data):
        return queries

