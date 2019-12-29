from django import forms
from django.forms import ModelForm
from .models import Manufacturer, ManufacturerLogo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions


class ManufacturerLogoForm(ModelForm):
    logo = forms.FileField(required=False)

    class Meta:
        model = ManufacturerLogo
        fields = ["logo"]

    def __init__(self, *args, **kwargs):
        super(ManufacturerLogoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class ManufacturerForm(ModelForm):
    name = forms.CharField()
    address = forms.CharField(required=False)
    url = forms.URLField(required=False)
    email = forms.EmailField(required=False)
    comment = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    fax = forms.CharField(required=False)

    class Meta:
        model = Manufacturer
        fields = ["name", "address", "url", "email", "comment", "phone", "fax"]

    def __init__(self, *args, **kwargs):
        super(ManufacturerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Field("name"),
            Field("address"),
            Field("url"),
            Field("email"),
            Field("comment"),
            Field("phone"),
            Field("fax"),
            FormActions(
                Submit("manufacturer_form", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-default' href='{% url \"manufacturer_list\" %}'>Cancel</a>"),
            ),
        )
