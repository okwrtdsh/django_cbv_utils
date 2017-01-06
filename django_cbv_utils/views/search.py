from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from django_cbv_utils.forms import SearchForm


class SearchListView(FormMixin, ListView):
    form_class = SearchForm
    context_search_form_name = 'form'

    def get_queryset(self):
        queryset = super().get_queryset().select_related()
        if not self.get_form_class():
            return queryset

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, queryset)
        else:
            return self.form_invalid(form, queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_search_form_name] = self.get_form()
        return context

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {
            'data': self.get_initial(),
            'prefix': self.get_prefix(),
            'request': self.request,
        }
        if self.request.method == 'GET' and self.request.GET:
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def form_valid(self, form, queryset):
        """
        Returns the queryset in case of valid form.
        """
        return form.get_queryset(queryset)

    def form_invalid(self, form, queryset):
        """
        Returns the queryset in case of invalid form.
        """
        return form.get_invalid_queryset(queryset)
