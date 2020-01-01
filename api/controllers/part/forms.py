from controllers.footprints.models import Footprint
from controllers.part.models import PartUnit, ParametersUnit, Part, PartParameter
from controllers.storage.models import StorageLocation
from controllers.part.forms_widgets import GroupedModelChoiceField
from crispy_forms.bootstrap import FormActions, Tab, TabHolder, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field, Fieldset, Row
from django import forms
from django.forms import ModelForm
from controllers.categories.models import Category
from mptt.forms import TreeNodeChoiceField
from .custom_layout_object import Formset
from django.forms.models import inlineformset_factory
import re


class PartUnitForm(ModelForm):
    name = forms.CharField()
    short_name = forms.CharField()
    description = forms.CharField(required=False)

    class Meta:
        model = PartUnit
        fields = ["name", "short_name", "description"]

    def __init__(self, *args, **kwargs):
        super(PartUnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Field("name"),
            Field("short_name"),
            Field("description"),
            FormActions(
                Submit("part_unit_list", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-default' href='{% url \"part_unit_list\" %}'>Cancel</a>"),
            ),
        )


class ParametersUnitForm(ModelForm):
    name = forms.CharField()
    symbol = forms.CharField(required=False)
    prefix = forms.CharField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        model = ParametersUnit
        fields = ["name", "prefix", "symbol", "description"]

    def __init__(self, *args, **kwargs):
        super(ParametersUnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Field("name"),
            Field("prefix"),
            Field("symbol"),
            Field("description"),
            FormActions(
                Submit("parameters_unit_list", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-default' href='{% url \"parameters_unit_list\" %}'>Cancel</a>"),
            ),
        )


class PartForm(ModelForm):
    class Meta:
        model = Part
        fields = [
            "name",
            "description",
            "comment",
            "stock_qty",
            "stock_qty_min",
            "needs_review",
            "condition",
            "can_be_sold",
            "private",
        ]

    name = forms.CharField()
    description = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    stock_qty = forms.IntegerField(initial=1)
    stock_qty_min = forms.IntegerField(initial=0)
    needs_review = forms.BooleanField(required=False, initial=False)
    condition = forms.CharField(required=False)
    can_be_sold = forms.BooleanField(required=False, initial=False)
    private = forms.BooleanField(required=False, initial=False)
    production_remarks = forms.CharField(required=False)
    status = forms.CharField(required=False)
    internal_part_number = forms.CharField(required=False)

    footprint = GroupedModelChoiceField(
        required=False, queryset=Footprint.objects.prefetch_related("footprint").all(), group_by_field="footprint"
    )
    category = TreeNodeChoiceField(required=False, queryset=Category.objects.all(), level_indicator=u"+--")
    part_unit = forms.ModelChoiceField(required=False, queryset=PartUnit.objects.all())
    storage = GroupedModelChoiceField(
        required=False, queryset=StorageLocation.objects.prefetch_related("category").all(), group_by_field="category"
    )

    # part attachment

    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)

        self.fields["storage"].label = "Storage Location"
        self.fields["status"].label = "Sheet Status"

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-4"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    "Basic parts informations",
                    Field("name"),
                    Field("description"),
                    Field("stock_qty"),
                    Field("stock_qty_min"),
                    Field("part_unit"),
                    Field("category"),
                    Field("storage"),
                    Field("footprint"),
                    Field("comment"),
                    Field("production_remarks"),
                    Field("status"),
                    Field("needs_review"),
                    Field("condition"),
                    Field("can_be_sold"),
                    Field("private"),
                    Field("internal_part_number"),
                    FormActions(
                        Submit("submit", "Save changes", css_class="btn-primary"),
                        HTML("<a class='btn btn-default' href='{% url \"part_list\" %}'>Cancel</a>"),
                    ),
                ),
                css_class="col-lg-6",
            ),
            Div(
                TabHolder(
                    Tab("Parameters", Formset("part_parameters")),
                    Tab("Manufacturers", Formset("part_manufacturers")),
                    Tab("Distributors", Formset("distributors_sku")),
                ),
                css_class="col-lg-6",
            ),
        )


class PartQuickAddForm(ModelForm):
    class Meta:
        model = Part
        fields = [
            "name",
            "description",
            "comment",
            "stock_qty",
            "stock_qty_min",
            "needs_review",
            "condition",
            "can_be_sold",
            "private",
        ]

    name = forms.CharField()
    description = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    stock_qty = forms.IntegerField(initial=1)
    stock_qty_min = forms.IntegerField(initial=0)
    needs_review = forms.BooleanField(required=False, initial=False)
    condition = forms.CharField(required=False)
    can_be_sold = forms.BooleanField(required=False, initial=False)
    private = forms.BooleanField(required=False, initial=False)
    status = forms.CharField(required=False)
    internal_part_number = forms.CharField(required=False)

    footprint = GroupedModelChoiceField(
        required=False, queryset=Footprint.objects.prefetch_related("footprint").all(), group_by_field="footprint"
    )
    category = TreeNodeChoiceField(required=False, queryset=Category.objects.all(), level_indicator=u"+--")
    part_unit = forms.ModelChoiceField(required=False, queryset=PartUnit.objects.all())
    storage = GroupedModelChoiceField(
        required=False, queryset=StorageLocation.objects.prefetch_related("category").all(), group_by_field="category"
    )

    # part attachment

    def __init__(self, *args, **kwargs):
        super(PartQuickAddForm, self).__init__(*args, **kwargs)

        self.fields["storage"].label = "Storage Location"
        self.fields["status"].label = "Sheet Status"

        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-4"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Div(
                Fieldset(
                    "Basic parts informations",
                    Field("name"),
                    Field("description"),
                    Field("stock_qty"),
                    Field("stock_qty_min"),
                    Field("status"),
                    Field("needs_review"),
                    Field("condition"),
                    Field("can_be_sold"),
                    Field("private"),
                    Field("internal_part_number"),
                ),
                css_class="col-lg-6",
            ),
            Div(
                Fieldset(
                    "&nbsp;",
                    Field("part_unit"),
                    Field("category"),
                    Field("storage"),
                    Field("footprint"),
                    FormActions(
                        Submit("submit", "Save changes", css_class="btn-primary"),
                        HTML("<a class='btn btn-default' href='{% url \"part_list\" %}'>Cancel</a>"),
                    ),
                ),
                css_class="col-lg-6",
            ),
        )


class PartParameterForm(ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)
    value = forms.CharField(required=True)
    unit = forms.ModelChoiceField(required=False, queryset=ParametersUnit.objects.all())

    class Meta:
        model = PartParameter
        fields = ["name", "description", "value", "unit"]

    def __init__(self, *args, **kwargs):
        super(PartParameterForm, self).__init__(*args, **kwargs)

        formtag_prefix = re.sub("-[0-9]+$", "", kwargs.get("prefix", ""))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Div(Row(Field("name"), Field("description")),),
            Row(Div(Field("value"), css_class="col-lg-6"), Div(Field("unit"), css_class="col-lg-6"),),
            Row(Field("DELETE"), css_class="formset_row-{}".format(formtag_prefix),),
        )


PartParameterFormSet = inlineformset_factory(
    Part,
    PartParameter,
    form=PartParameterForm,
    fields=["name", "description", "value", "unit"],
    extra=1,
    can_delete=True,
)
