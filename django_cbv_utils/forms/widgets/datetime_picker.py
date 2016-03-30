# Dependent on https://github.com/Eonasdan/bootstrap-datetimepicker
import re
from django.forms import forms
from django.forms.widgets import DateTimeBaseInput,\
     DateTimeInput, DateInput, TimeInput
from django.utils.safestring import mark_safe
from django.utils.six import string_types


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

ID_RE = re.compile(r'id=\"([a-z_]+)\"')


def to_js_value(key, value):
    if isinstance(value, string_types):
        return "'%s'" % value
    if isinstance(value, bool):
        return {True:'true',False:'false'}[value]
    return value


class DateTimePickerBaseMixin(DateTimeBaseInput):
    DATETIMEPICKER_TEMPLATE = """
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
      </div>
    """

    glyphicon = None

    def __init__(self, attrs=None, options=None):
        if attrs is None:
            attrs = {}
        self.attrs = attrs
        self.options = options
        self.format = None

        format = self.options['format']
        self.format = TO_PYTHON_RE.sub(
            lambda x: TO_PYTHON_FMT[x.group()],
            format
        )
        super(DateTimePickerBaseMixin, self).__init__(attrs, format=self.format)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        rendered_widget = super(DateTimePickerBaseMixin, self).render(name, value, final_attrs)

        options_list = []
        for key, value in iter(self.options.items()):
            options_list.append("%s: %s" % (key, to_js_value(key, value)))
        js_options = ",\n".join(options_list)

        return mark_safe(
            self.DATETIMEPICKER_TEMPLATE.format(
                id=self.get_id(final_attrs),
                rendered_widget=rendered_widget,
                options=js_options
            )
        )

    def get_id(self, final_attrs):
        return final_attrs["id"]

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
        super(DateTimePickerWidget, self).__init__(attrs, options)


class DatePickerWidget(DateTimePickerBaseMixin, DateInput):

    def __init__(self, attrs={}, options={}):
        options['format'] = options.get('format', 'YYYY-MM-DD')
        options['locale'] = options.get('locale', 'ja')
        options['viewMode'] = options.get('viewMode', "days")
        super(DatePickerWidget, self).__init__(attrs, options)


class TimePickerWidget(DateTimePickerBaseMixin, TimeInput):

    def __init__(self, attrs={}, options={}):
        options['format'] = options.get('format', 'HH:mm')
        options['locale'] = options.get('locale', 'ja')
        super(TimePickerWidget, self).__init__(attrs, options)

