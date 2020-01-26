from django import forms
from django.forms import ModelForm
from .models import Manufacturer, ManufacturerLogo, PartManufacturer
from controllers.part.models import Part
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Row, Div, Fieldset, Column
from crispy_forms.bootstrap import FormActions
from django.forms.models import inlineformset_factory
import re
from controllers.part.custom_layout_object import Formset

FormActions.template = "form_actions_tmpl.html"


class ManufacturerLogoForm(ModelForm):
    logo = forms.FileField(required=False)

    class Meta:
        model = ManufacturerLogo
        fields = ["logo"]

    def __init__(self, *args, **kwargs):
        super(ManufacturerLogoForm, self).__init__(*args, **kwargs)

        formtag_prefix = re.sub("-[0-9]+$", "", kwargs.get("prefix", ""))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-3"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Div(Row(Field("logo")),), Row(Field("DELETE"), css_class="formset_row-{}".format(formtag_prefix),),
        )


class ManufacturerForm(ModelForm):
    name = forms.CharField(required=True)
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
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Div(
                Div(
                    Fieldset(
                        "Manufacturer informations",
                        Field("name"),
                        Field("address"),
                        Field("url"),
                        Field("email"),
                        Field("comment"),
                        Field("phone"),
                        Field("fax"),
                        FormActions(
                            Submit("submit", "Save changes", css_class="btn-primary"),
                            HTML("<a class='btn btn-light' href='{% url \"manufacturer_list\" %}'>Cancel</a>"),
                        ),
                    ),
                    css_class="col-lg-6",
                ),
                Div(Fieldset("Logos", Formset("manufacturer_logos")), css_class="col-lg-6"),
                css_class="form-group row",
            )
        )
        self.is_multipart = True


class PartManufacturerForm(ModelForm):
    sku = forms.CharField()
    manufacturer = forms.ModelChoiceField(required=False, queryset=PartManufacturer.objects.all())

    class Meta:
        model = PartManufacturer
        fields = ["sku", "manufacturer"]

    def __init__(self, *args, **kwargs):
        super(PartManufacturerForm, self).__init__(*args, **kwargs)

        formtag_prefix = re.sub("-[0-9]+$", "", kwargs.get("prefix", ""))

        self.fields["sku"].label = "SKU"

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-3"
        self.helper.field_class = "col-sm-9"
        self.helper.layout = Layout(
            Div(
                Field("sku"),
                Field("manufacturer"),
                Row(Column(css_class="col-lg-6 delete-here-manuf"), css_class="row"),
                Field("DELETE"),
                css_class="formset_row-{}".format(formtag_prefix),
            )
        )


PartManufacturerFormSet = inlineformset_factory(
    Part, PartManufacturer, form=PartManufacturerForm, fields=["sku", "manufacturer"], extra=1, can_delete=True
)

ManufacturerLogoFormSet = inlineformset_factory(
    Manufacturer, ManufacturerLogo, form=ManufacturerLogoForm, fields=["logo"], extra=1, can_delete=True
)
