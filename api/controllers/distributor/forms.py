from django import forms
from django.forms import ModelForm
from .models import Distributor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions


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
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Field("sku"),
            Field("distributor"),
            FormActions(Submit("distributor_sku_create", "Save changes", css_class="btn-primary")),
        )
