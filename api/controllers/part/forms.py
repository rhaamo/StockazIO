from controllers.footprints.models import Footprint
from controllers.part.models import PartUnit, ParametersUnit, Part
from controllers.part.forms_widgets import GroupedModelChoiceField
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field
from django import forms
from django.forms import ModelForm


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

    footprint = GroupedModelChoiceField(required=False, queryset=Footprint.objects.all(), group_by_field="footprint")
    part_unit = forms.ModelChoiceField(required=False, queryset=PartUnit.objects.all())

    # tags
    # part parameters
    # part attachment

    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-2"
        self.helper.field_class = "col-sm-8"
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            Field("comment"),
            Field("stock_qty"),
            Field("stock_qty_min"),
            Field("needs_review"),
            Field("condition"),
            Field("can_be_sold"),
            Field("private"),
            Field("footprint"),
            Field("part_unit"),
            FormActions(
                Submit("part_list", "Save changes", css_class="btn-primary"),
                HTML("<a class='btn btn-default' href='{% url \"part_list\" %}'>Cancel</a>"),
            ),
        )
