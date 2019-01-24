# Dependent on https://github.com/Eonasdan/bootstrap-datetimepicker
import re

from django.forms import forms
from django.forms.widgets import (
    DateInput, DateTimeBaseInput, DateTimeInput, TimeInput,
)
from django.utils.safestring import mark_safe

from .misc import to_js_value

# http://momentjs.com/docs/#/parsing/string-format/
TO_PYTHON_FMT = {
    'ddd': '%a',
    'dddd': '%A',
    'DD': '%d',
    'D': '%-d',
    'MMM': '%b',
    'MMMM': '%B',
    'MM': '%m',
    'M': '%-m',
    'YY': '%y',
    'YYYY': '%Y',
    'HH': '%H',
    'hh': '%I',
    'A': '%p',
    'mm': '%M',
    'ss': '%S',
    'SSSSSS': '%f',
    'Z': '%z',
    'DDDD': '%j',
    'ww': '%U',
    'WW': '%W',
}

TO_PYTHON_RE = re.compile(r'\b(' + '|'.join(TO_PYTHON_FMT.keys()) + r')\b')


class DateTimePickerBaseMixin(DateTimeBaseInput):
    DATETIMEPICKER_TEMPLATE = {
        False: """
        <div class="row">
          <div class='col-sm-12'>
            {rendered_widget}
          </div>
          <script type="text/javascript">
            $(function () {{
              $("#{id}").datetimepicker({{{options}}});
            }});
          </script>
        </div>
        """,
        True: """
        <div class="row">
          <div class='col-sm-12'>
            <div class="form-group">
              <div class='input-group' id="{id}">
                {rendered_widget}
                <span class="input-group-addon">
                  <span class="glyphicon {glyphicon}"></span>
                </span>
              </div>
            </div>
          </div>
          <script type="text/javascript">
            $(function () {{
              $("div#{id}").datetimepicker({{{options}}});
            }});
          </script>
        </div>
        """
    }

    glyphicon = None

    def __init__(self, attrs=None, options=None):
        if attrs is None:
            attrs = {}
        self.attrs = attrs
        self.options = options
        self.format = None
        self.glyphicon = self.options.pop("glyphicon", None)

        format = self.options['format']
        self.format = TO_PYTHON_RE.sub(
            lambda x: TO_PYTHON_FMT[x.group()],
            format
        )
        super().__init__(attrs, format=self.format)

    def render(self, name, value, attrs=None, renderer=None):
        final_attrs = self.build_attrs(attrs)
        rendered_widget = super().render(name, value, final_attrs)

        options_list = []
        for key, value in iter(self.options.items()):
            options_list.append("%s: %s" % (key, to_js_value(key, value)))
        js_options = ",\n".join(options_list)

        return mark_safe(
            self.DATETIMEPICKER_TEMPLATE[self.has_glyphicon].format(
                id=self.get_id(final_attrs),
                rendered_widget=rendered_widget,
                options=js_options,
                glyphicon=self.glyphicon
            )
        )

    def get_id(self, final_attrs):
        return final_attrs["id"]

    @property
    def has_glyphicon(self):
        return self.glyphicon is not None

    @property
    def media(self):
        """
        Require
        * jquery.min.js
        * bootstrap.min.js
        * bootstrap.min.css
        """
        js = [
            "moment/moment.min.js",
            "moment/moment-with-locales.min.js",
            "eonasdan-bootstrap-datetimepicker/js/bootstrap-datetimepicker.min.js",
        ]
        locale = self.options.get('locale', 'en')
        if locale != 'en':
            js.append("moment/locale/%s.js" % locale)
        return forms.Media(
            css={
                'all': (
                    'eonasdan-bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css',)
            },
            js=js
        )


class DateTimePickerWidget(DateTimePickerBaseMixin, DateTimeInput):

    def __init__(self, attrs={}, options={}):
        options['format'] = options.get('format', 'YYYY-MM-DD HH:mm')
        options['locale'] = options.get('locale', 'ja')
        options['viewMode'] = options.get('viewMode', "days")
        options['sideBySide'] = options.get('sideBySide', True)
        super().__init__(attrs, options)


class DatePickerWidget(DateTimePickerBaseMixin, DateInput):

    def __init__(self, attrs={}, options={}):
        options['format'] = options.get('format', 'YYYY-MM-DD')
        options['locale'] = options.get('locale', 'ja')
        options['viewMode'] = options.get('viewMode', "days")
        super().__init__(attrs, options)


class TimePickerWidget(DateTimePickerBaseMixin, TimeInput):

    def __init__(self, attrs={}, options={}):
        options['format'] = options.get('format', 'HH:mm')
        options['locale'] = options.get('locale', 'ja')
        super().__init__(attrs, options)
