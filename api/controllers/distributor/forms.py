from django import forms
from django.forms import ModelForm
from .models import Distributor, DistributorSku
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Div, Row, Column
from crispy_forms.bootstrap import FormActions
from django.forms.models import inlineformset_factory
from controllers.part.models import Part
import re

FormActions.template = "form_actions_tmpl.html"


class DistributorForm(ModelForm):
    name = forms.CharField()
    address = forms.CharField(required=False)
    url = forms.URLField(required=False)
    email = forms.EmailField(required=False)
    comment = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    fax = forms.CharField(required=False)

    class Meta:
        model = Distributor
        fields = ["name", "address", "url", "email", "comment", "phone", "fax"]

    def __init__(self, *args, **kwargs):
        super(DistributorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-4"
        self.helper.layout = Layout(
            Field("name"),
            Field("address"),
            Field("url"),
            Field("email"),
            Field("comment"),
            Field("phone"),
            Field("fax"),
            FormActions(
                Submit("distributor_create", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-light' href='{% url \"distributor_list\" %}'>Cancel</a>"),
            ),
        )


class DistributorSkuForm(ModelForm):
    sku = forms.CharField()
    distributor = forms.ModelChoiceField(required=True, queryset=Distributor.objects.all())

    class Meta:
        model = DistributorSku
        fields = ["sku", "distributor"]

    def __init__(self, *args, **kwargs):
        super(DistributorSkuForm, self).__init__(*args, **kwargs)

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
                Field("distributor"),
                Row(Column(css_class="col-lg-6 delete-here-distrib"), css_class="row"),
                Field("DELETE"),
                css_class="formset_row-{}".format(formtag_prefix),
            )
        )


DistributorSkuFormSet = inlineformset_factory(
    Part, DistributorSku, form=DistributorSkuForm, fields=["sku", "distributor"], extra=1, can_delete=True
)
