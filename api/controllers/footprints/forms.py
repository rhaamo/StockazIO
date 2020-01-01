from django import forms
from django.forms import ModelForm
from .models import Footprint, FootprintCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions


class FootprintCategoryForm(ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)

    class Meta:
        model = FootprintCategory
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(FootprintCategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-4"
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            FormActions(
                Submit("footprint_category_create", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-light' href='{% url \"footprint_category_list\" %}'>Cancel</a>"),
            ),
        )


class FootprintForm(ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)
    picture = forms.FileField(required=False)

    class Meta:
        model = Footprint
        fields = ["name", "description", "picture"]

    def __init__(self, *args, **kwargs):
        super(FootprintForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-4"
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            Field("picture"),
            FormActions(Submit("footprint_create", "Save changes", css_class="btn-primary"),),
        )
