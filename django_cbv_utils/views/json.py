from django.http.response import JsonResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.edit import FormView


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class JSONView(JSONResponseMixin, TemplateView):

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class FormJSONResponseView(JSONResponseMixin, FormView):

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_json_response(self.get_context_data(form=form), safe=False)


class HybridJSONResponseMixin(JSONResponseMixin, TemplateResponseMixin):
    sign = "format"
    countersign = "json"

    def render_to_response(self, context):
        if self.request.GET.get(self.sign) == self.countersign:
            return self.render_to_json_response(context)
        else:
            return super(HybridJSONResponseMixin, self).render_to_response(context)
