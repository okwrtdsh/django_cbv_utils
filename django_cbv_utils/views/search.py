import re
import datetime
from django.db.models import Q
from django.views.generic.list import ListView
from django_cbv_utils.forms import SearchForm


class SearchListView(ListView):
    form = SearchForm

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


    def get_queryset(self):
        queryset = super(SearchListView, self).get_queryset().select_related()
        if not self.form:
            return queryset

        bound_form = self.form(self.request.GET)
        if not bound_form.is_valid():
            return queryset

        queries = Q()
        queries &= self.get_queries(bound_form, self.form.queryset_filter)
        queries &= ~self.get_queries(bound_form, self.form.queryset_exclude)
        return queryset.filter(queries).distinct()

    def get_queries(self, bound_form, filter):
        queries = Q()
        for target, filter_dict in filter.items():
            operator = filter_dict.get('op', '')
            if len(filter_dict['flds']) > 1:
                content = []
                for field in filter_dict['flds']:
                    content.append(bound_form.cleaned_data[field])
            else:
                content = bound_form.cleaned_data[filter_dict['flds'][0]]
                if content is None:
                    continue

            if not operator:
                queries &= Q(**{target: content})
                continue

            if operator not in self.custom_lookup:
                queries &= Q(**{'{0}__{1}'.format(
                    target, operator): content})
                continue

            if operator == 'or':
                q = Q()
                for v in content:
                    if v is not None:
                        q |= Q(**{target: v})
                queries &= q
                continue

            if operator == 'date':
                if not isinstance(content, datetime.date):
                    continue
                queries &= Q(**{'{0}__{1}'.format(target, attr): getattr(
                    content, attr) for attr in ("year", "month", "day")})
                continue

            if operator in ('gt_lt', 'gt_lte', 'gte_lt', 'gte_lte'):
                q = Q()
                for i, v in enumerate(content):
                    if v is not None:
                        q &= Q(**{'{0}__{1}'.format(
                            target, operator.split("_")[i]): v})
                queries &= q
                continue

            if operator == "icontains_or":
                q = Q()
                for v in re.split("\s", content):
                    q |= Q(**{'{0}__icontains'.format(target): v})
                queries &= q
                continue

            if operator == "icontains_and":
                if not isinstance(content, str) or not content:
                    continue
                queries &= Q(**{'{0}__icontains'.format(target): v
                    for v in re.split("\s", content)})
                continue

        return queries

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['form'] = self.form(self.request.GET)
        return context

