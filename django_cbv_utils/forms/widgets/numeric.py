# Dependent on https://github.com/SamWM/jQuery-Plugins/tree/master/numeric
from django.forms.widgets import NumberInput
from django.utils.safestring import mark_safe

from .misc import to_js_value


class NumericWidget(NumberInput):
    NUMERIC_TEMPLATE = """
        <div class="row">
          <div class='col-sm-12'>
            {rendered_widget}
          </div>
          <script type="text/javascript">
            $(function () {{
              $("#{id}").numeric({{
                {options}
              }}).change(function() {{
                $(this).keyup();
              }});
            }});
          </script>
        </div>
        """

    class Media:
        js = ["numeric/jquery.numeric.min.js"]

    def __init__(self, attrs={}, options={}):
        self.attrs = attrs
        self.options = options
        super().__init__(attrs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        rendered_widget = super().render(name, value, final_attrs)

        options_list = []
        for key, value in iter(self.options.items()):
            options_list.append("%s: %s" % (key, to_js_value(key, value)))
        js_options = ",\n".join(options_list)

        return mark_safe(
            self.NUMERIC_TEMPLATE.format(
                id=self.get_id(final_attrs),
                rendered_widget=rendered_widget,
                options=js_options,
            )
        )

    def get_id(self, final_attrs):
        return final_attrs["id"]


class NumericIntegerWidget(NumericWidget):

    def __init__(self, attrs={}, options={}):
        options['decimal'] = options.get('decimal', False)
        super().__init__(attrs, options)


class NumericPositiveIntegerWidget(NumericWidget):

    def __init__(self, attrs={}, options={}):
        options['decimal'] = options.get('decimal', False)
        options['negative'] = options.get('negative', False)
        super().__init__(attrs, options)
