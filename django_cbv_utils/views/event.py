from django.views.generic.base import View


class GETBindEventMixin(View):
    """
    get_key = "action"
    get_events = {"myevent": "myfunc"}

    def myfunc(self, request, *args, **kwargs):
    """

    get_key = "action"
    get_events = {}

    def get(self, request, *args, **kwargs):
        key = request.GET.get(self.get_key)
        handler = getattr(
            super(GETBindEventMixin, self), "get", self.http_method_not_allowed)
        if key is not None and self.get_events.get(key):
            handler = getattr(self, self.get_events[key], handler)
        return handler(request, *args, **kwargs)


class POSTBindEventMixin(View):
    """
    post_key = "action"
    post_events = {"myevent": "myfunc"}

    def myfunc(self, request, *args, **kwargs):
    """

    post_key = "action"
    post_events = {}

    def post(self, request, *args, **kwargs):
        key = request.POST.get(self.post_key)
        handler = getattr(
            super(POSTBindEventMixin, self), "post", self.http_method_not_allowed)
        if key is not None and self.post_events.get(key):
            handler = getattr(self, self.post_events[key], handler)
        return handler(request, *args, **kwargs)
