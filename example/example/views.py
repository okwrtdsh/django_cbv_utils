from django.shortcuts import redirect
from example.forms import MyModelSearchForm
from example.models import MyModel

from django_cbv_utils.views import (
    GETBindEventMixin, JSONResponseMixin, POSTBindEventMixin, SearchListView,
)


class MyModelListView(
        GETBindEventMixin, POSTBindEventMixin,
        JSONResponseMixin, SearchListView):
    model = MyModel
    form_class = MyModelSearchForm
    context_object_name = "mymodels"
    paginate_by = 20
    template_name = "list.html"
    get_key = "action"
    get_events = {"echo": "hello_world"}
    post_key = "reset_button"
    post_events = {"reset": "reset"}

    def hello_world(self, request, *args, **kwargs):
        return self.render_to_json_response({"hello": "world"})

    def reset(self, request, *args, **kwargs):
        return redirect("list")
