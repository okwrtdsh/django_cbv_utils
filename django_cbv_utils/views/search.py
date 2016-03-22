from django.views.generic.list import ListView
from django_cbv_utils.forms import SearchForm


class SearchListView(ListView):
    form_class = SearchForm

    def get_queryset(self):
        queryset = super(SearchListView, self).get_queryset().select_related()
        if not self.form_class:
            return queryset

        form = self.form_class(self.request.GET)
        if not form.is_valid():
            return queryset

        queryset = form.get_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context

