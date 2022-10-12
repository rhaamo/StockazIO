import factory

from controllers.categories.factories import CategoryFactory
from controllers.distributor.factories import DistributorFactory
from controllers.factories import registry
from controllers.manufacturer.factories import ManufacturerFactory


@registry.register
class OrdersImporterOrderFactory(factory.django.DjangoModelFactory):
    date = factory.Faker("date_time_this_month")
    order_number = factory.Faker("bothify", text="######")
    vendor_db = factory.SubFactory(DistributorFactory)
    status = "Fetched"
    import_state = 1  # Fetched

    class Meta:
        model = "OrdersImporter.Order"
        django_get_or_create = ("order_number",)


@registry.register
class OrdersImporterItemFactory(factory.django.DjangoModelFactory):
    vendor_part_number = factory.Faker("bothify", text="vdr-capacitor-######")
    mfr_part_number = factory.Faker("bothify", text="mfr-capacitor-######")
    manufacturer = factory.Faker("company")
    manufacturer_db = factory.SubFactory(ManufacturerFactory)
    description = factory.Faker("bs")
    quantity = factory.Faker("random_int", min=10, max=128)
    order = factory.SubFactory(OrdersImporterOrderFactory)

    class Meta:
        model = "OrdersImporter.Item"
        django_get_or_create = ("vendor_part_number",)


@registry.register
class OrdersImporterCategoryMatcherFactory(factory.django.DjangoModelFactory):
    regexp = factory.Faker("random_element", elements=["capacitor"])
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = "OrdersImporter.CategoryMatcher"
        django_get_or_create = ("regexp",)
