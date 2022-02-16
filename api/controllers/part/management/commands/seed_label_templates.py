from django.core.management.base import BaseCommand
from controllers.labeltemplate.models import LabelTemplate


class Command(BaseCommand):
    help = """ Seed Label Templates """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        print("Seeding Label Templates...")
        templates = [
            {
                "name": "Brother 12mm",
                "width": 90,
                "height": 12,
                "text_template": "{name}",
                "template": '{ "qrcode": { "type": "qrcode", "position": { "x": 1, "y": 1 }, "width": 10, "height": 10 }, "text": { "type": "text", "position": { "x": 12, "y": 1 }, "width": 44.61, "height": 10, "alignment": "left", "fontSize": 12, "characterSpacing": 0, "lineHeight": 1 } }',
            },
            {
                "name": "Brother 90x38",
                "width": 90,
                "height": 38,
                "text_template": """{name}
{description}""",
                "template": '{ "qrcode": { "type": "qrcode", "position": { "x": 1, "y": 1 }, "width": 36, "height": 36 }, "text": { "type": "text", "position": { "x": 39.39, "y": 1 }, "width": 44.61, "height": 34, "alignment": "left", "fontSize": 12, "characterSpacing": 0, "lineHeight": 1 } }',
            },
        ]
        for item in templates:
            try:
                tpl = LabelTemplate.objects.get(
                    name=item["name"],
                    width=item["width"],
                    height=item["height"],
                    text_template=item["text_template"],
                    template=item["template"],
                )
            except LabelTemplate.DoesNotExist:
                tpl = LabelTemplate(
                    name=item["name"],
                    width=item["width"],
                    height=item["height"],
                    text_template=item["text_template"],
                    template=item["template"],
                )
                tpl.save()
            except LabelTemplate.MultipleObjectsReturned:
                print(f"WARNING: Multiple entries returned for {item.name!r}, {item.width!r}*{item.height!r}, skipping")
                continue
