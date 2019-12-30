from django import forms
from django.forms import ModelForm
from .models import Distributor, DistributorSku
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Row
from crispy_forms.bootstrap import FormActions
from django.forms.models import inlineformset_factory
from controllers.part.models import Part
import re


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
                Submit("distributor_create", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-default' href='{% url \"distributor_list\" %}'>Cancel</a>"),
            ),
        )


class DistributorSkuForm(ModelForm):
    sku = forms.CharField()
    distributor = forms.ModelChoiceField(required=False, queryset=Distributor.objects.all())

    class Meta:
        model = Distributor
        fields = ["sku", "distributor"]

    def __init__(self, *args, **kwargs):
        super(DistributorSkuForm, self).__init__(*args, **kwargs)

        formtag_prefix = re.sub("-[0-9]+$", "", kwargs.get("prefix", ""))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Row(Field("sku"), Field("distributor"), Field("DELETE"), css_class="formset_row-{}".format(formtag_prefix))
        )


DistributorSkuFormSet = inlineformset_factory(
    Part, DistributorSku, form=DistributorSkuForm, fields=["sku", "distributor"], extra=1, can_delete=True
)
