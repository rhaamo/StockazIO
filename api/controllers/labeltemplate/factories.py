import factory

from controllers.factories import registry


@registry.register
class LabelTemplateFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    width = factory.Faker("random_int", min=10, max=128)
    height = factory.Faker("random_int", min=10, max=128)
    template = """{ "qrcode": { "type": "qrcode", "position": { "x": 1, "y": 1 }, "width": 10, "height": 10 }, "text": { "type": "text", "position": { "x": 12, "y": 1 }, "width": 44.61, "height": 10, "alignment": "left", "fontSize": 12, "characterSpacing": 0, "lineHeight": 1 } }
    """
    text_template = """{name}
{description}"""

    class Meta:
        model = "labeltemplate.LabelTemplate"
        django_get_or_create = ("name",)
