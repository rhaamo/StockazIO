import factory

from controllers.categories.factories import CategoryFactory
from controllers.factories import registry
from controllers.footprints.factories import FootprintFactory
from controllers.storage.factories import StorageFactory


@registry.register
class PartUnitFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    short_name = factory.Faker("text")
    description = factory.Faker("text")

    class Meta:
        model = "part.PartUnit"


@registry.register
class PartFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")
    stock_qty_min = factory.Faker("random_int", min=10, max=128)
    stock_qty = factory.Faker("random_int", min=10, max=128)
    part_unit = factory.SubFactory(PartUnitFactory)
    category = factory.SubFactory(CategoryFactory)
    storage = factory.SubFactory(StorageFactory)
    footprint = factory.SubFactory(FootprintFactory)
    comment = factory.Faker("text")
    production_remarks = factory.Faker("text")
    status = factory.Faker("text")
    needs_review = factory.Faker("boolean")
    condition = factory.Faker("text")
    can_be_sold = factory.Faker("boolean")
    private = factory.Faker("boolean")
    internal_part_number = factory.Faker("bothify", text="mfr-capacitor-######")

    class Meta:
        model = "part.Part"


# @registry.register
# class PartAttachmentTypeFileFactory(factory.django.DjangoModelFactory):
#     description = factory.Faker("text")
#     file = factory.django.FileField(type="text")
#     part = factory.SubFactory(PartFactory)

#     class Meta:
#         model = "part.PartAttachment"


@registry.register
class PartAttachmentTypePictureFactory(factory.django.DjangoModelFactory):
    description = factory.Faker("text", max_nb_chars=99)
    picture = factory.django.ImageField(from_path="../setup-data/manufacturers/images/st.png")
    picture_default = factory.Faker("boolean")
    part = factory.SubFactory(PartFactory)

    class Meta:
        model = "part.PartAttachment"


@registry.register
class ParametersUnitsFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    symbol = factory.Faker("name")
    description = factory.Faker("text")

    class Meta:
        model = "part.ParametersUnit"


@registry.register
class PartParameterPresetFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = "part.PartParameterPreset"


@registry.register
class PartParameterPresetItemFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")
    unit = factory.SubFactory(ParametersUnitsFactory)
    part_parameter_preset = factory.SubFactory(PartParameterPresetFactory)

    class Meta:
        model = "part.PartParameterPresetItem"


@registry.register
class PartParameterFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text")
    value = factory.Faker("name")
    unit = factory.SubFactory(ParametersUnitsFactory)
    part = factory.SubFactory(PartFactory)

    class Meta:
        model = "part.PartParameter"
