import datetime
import re

from django.db.models import Q
from django.forms import ModelForm


class SearchForm(ModelForm):
    queryset_filter = None
    queryset_exclude = None
    require_fields = None

    lookups = [
        'or',
        'date',  # TODO: remove in Django 1.9
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
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = field in self.get_require_fields()

    def get_queryset_filter(self):
        if self.queryset_filter is not None:
            return self.queryset_filter
        return []

    def get_queryset_exclude(self):
        if self.queryset_exclude is not None:
            return self.queryset_exclude
        return []

    def get_require_fields(self):
        if self.require_fields is not None:
            return self.require_fields
        return []

    def get_queryset(self, queryset):
        query = Q()
        query &= self.get_query_from_list(self.get_queryset_filter())
        query &= ~self.get_query_from_list(self.get_queryset_exclude())
        return queryset.filter(query).distinct()

    def get_invalid_queryset(self, queryset):
        return queryset.none()

    def get_operator(self, filter_dict):
        return filter_dict.get('op', '')

    def get_targets(self, filter_dict):
        targets = filter_dict['targets']
        if isinstance(targets, (tuple, list)):
            return targets
        return [targets]

    def get_fields(self, filter_dict):
        fields = filter_dict.get('fields')
        if fields is None:
            return self.get_targets(filter_dict)
        if isinstance(fields, (tuple, list)):
            return fields
        return [fields]

    def get_cleaned_data_list(self, fields, filter_dict):
        return [self.cleaned_data.get(field) for field in fields]

    def get_query_from_list(self, queryset_filter):
        query = Q()
        for filter_dict in queryset_filter:
            operator = self.get_operator(filter_dict)
            targets = self.get_targets(filter_dict)
            fields = self.get_fields(filter_dict)
            cleaned_data_list = self.get_cleaned_data_list(fields, filter_dict)
            if not cleaned_data_list:
                continue
            query &= self.get_query(operator, targets, cleaned_data_list)
        return query

    def get_query(self, operator, targets, cleaned_data_list):
        query = Q()
        if not operator:
            for target in targets:
                q = Q()
                for cleaned_data in cleaned_data_list:
                    if cleaned_data:
                        q &= Q(**{target: cleaned_data})
                query |= q
        elif operator not in self.lookups:
            for target in targets:
                q = Q()
                for cleaned_data in cleaned_data_list:
                    if cleaned_data:
                        q &= Q(**{'{0}__{1}'.format(
                            target, operator): cleaned_data})
                query |= q
        elif operator == 'or':
            for target in targets:
                q = Q()
                for cleaned_data in cleaned_data_list:
                    if cleaned_data:
                        q |= Q(**{target: cleaned_data})
                query |= q
        elif operator == 'date':
            dates = []
            for cleaned_data in cleaned_data_list:
                if isinstance(
                        cleaned_data, (datetime.date, datetime.datetime)):
                    dates.append(cleaned_data)
            for target in targets:
                q = Q()
                for date in dates:
                    q &= Q(**{'{0}__{1}'.format(target, attr): getattr(
                        date, attr) for attr in ('year', 'month', 'day')})
                query |= q
        elif operator in ('gt_lt', 'gt_lte', 'gte_lt', 'gte_lte'):
            for target in targets:
                q = Q()
                for i, cleaned_data in enumerate(cleaned_data_list):
                    if cleaned_data is not None and i < 2:
                        q &= Q(**{'{0}__{1}'.format(
                            target, operator.split('_')[i]): cleaned_data})
                query |= q
        elif operator == 'icontains_or':
            words = []
            for cleaned_data in cleaned_data_list:
                if isinstance(cleaned_data, str) and cleaned_data != '':
                    words.extend(re.split('\s', cleaned_data))
            for target in targets:
                q = Q()
                for word in words:
                    q |= Q(**{'{0}__icontains'.format(target): word})
                query |= q
        elif operator == 'icontains_and':
            words = []
            for cleaned_data in cleaned_data_list:
                if isinstance(cleaned_data, str) and cleaned_data != '':
                    words.extend(re.split('\s', cleaned_data))
            for target in targets:
                q = Q()
                for word in words:
                    q &= Q(**{'{0}__icontains'.format(target): word})
                query |= q
        return query
