from django import forms
from django.forms import ModelForm
from .models import StorageLocation, StorageCategory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from crispy_forms.bootstrap import FormActions


class StorageForm(ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)

    class Meta:
        model = StorageLocation
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(StorageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-4"
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            FormActions(
                Submit("storage_category_form", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-light' href='{% url \"storage_category_list\" %}'>Cancel</a>"),
            ),
        )


class StorageCategoryForm(ModelForm):
    name = forms.CharField()
    description = forms.CharField(required=False)

    class Meta:
        model = StorageCategory
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(StorageCategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-4"
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            FormActions(
                Submit("storage_category_form", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-light' href='{% url \"storage_category_list\" %}'>Cancel</a>"),
            ),
        )
