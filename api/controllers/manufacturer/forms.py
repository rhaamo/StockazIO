from django import forms
from django.forms import ModelForm
from .models import Manufacturer, ManufacturerLogo, PartManufacturer
from controllers.part.models import Part
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Row
from crispy_forms.bootstrap import FormActions
from django.forms.models import inlineformset_factory
import re


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


class PartManufacturerForm(ModelForm):
    sku = forms.CharField()
    distributor = forms.ModelChoiceField(required=False, queryset=PartManufacturer.objects.all())

    class Meta:
        model = PartManufacturer
        fields = ["sku", "distributor"]

    def __init__(self, *args, **kwargs):
        super(PartManufacturerForm, self).__init__(*args, **kwargs)

        formtag_prefix = re.sub("-[0-9]+$", "", kwargs.get("prefix", ""))

        self.fields["sku"].label = "SKU"

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Row(Field("sku"), Field("manufacturer"), Field("DELETE"), css_class="formset_row-{}".format(formtag_prefix))
        )


PartManufacturerFormSet = inlineformset_factory(
    Part, PartManufacturer, form=PartManufacturerForm, fields=["sku", "manufacturer"], extra=1, can_delete=True
)
