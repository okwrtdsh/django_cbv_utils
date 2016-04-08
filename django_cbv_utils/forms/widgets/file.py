from django.forms.widgets import ClearableFileInput, CheckboxInput
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class BootstrapFileInputWidget(ClearableFileInput):
    template_with_initial = (
        '<div class="current_file"> '
        '  <div class="input-group"> '
        '    <div class="input-group-btn" role="group" data-toggle="buttons"> '
        '      <button type="button" class="btn btn-primary btn-secondary"> '
        '        %(initial_text)s '
        '      </button> '
        '    </div> '
        '    <a href="%(initial_url)s"> '
        '      <input type="text" class="form-control" readonly="readonly" value="%(initial)s"> '
        '    </a> '
        '    %(clear_template)s '
        '  </div> '
        '</div><br> '
        '<div class="select_file"> '
        '  <div class="input-group"> '
        '    <span class="input-group-btn"> '
        '      <span class="btn btn-primary btn-file form-control"> '
        '        %(input_text)s %(input)s '
        '      </span> '
        '    </span> '
        '    <input type="text" class="form-control" readonly="readonly"> '
        '  </div> '
        '</div> '
    )

    template_with_clear = (
        '<div class="input-group-btn" role="group" data-toggle="buttons"> '
        '  <label for="%(clear_checkbox_id)s" class="btn btn-default btn-secondary"> '
        '    %(clear)s %(clear_checkbox_label)s '
        '  </label> '
        '</div> '
    )

    class Media:
        js = ["bootstrap-filewidget/bootstrap-filewidget.js"]
        css = {
            'all': (
                "bootstrap-filewidget/bootstrap-filewidget.css",
            )
        }

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = (
            '<div class="select_file"> '
            '  <div class="input-group"> '
            '    <span class="input-group-btn"> '
            '      <span class="btn btn-primary btn-file form-control"> '
            '        %(input_text)s %(input)s '
            '      </span> '
            '    </span> '
            '    <input type="text" class="form-control" readonly="readonly"> '
            '  </div> '
            '</div> '
        )

        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

