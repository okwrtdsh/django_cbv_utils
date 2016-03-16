from django_cbv_utils.views import SearchListView
from example.models import MyModel
from example.forms import MyModelSearchForm


class MyModelListView(SearchListView):
    model = MyModel
    form_class = MyModelSearchForm
    context_object_name = "mymodels"
    paginate_by = 20
    template_name = "list.html"

