from urllib.parse import urlencode

from django.http.response import HttpResponseRedirect


class RedirectWithParamsMixin(object):
    params = {}

    def get_params(self, form=None):
        return self.params

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponseRedirect(
            self.get_success_url() + "?%s" % urlencode(self.get_params(form)))
