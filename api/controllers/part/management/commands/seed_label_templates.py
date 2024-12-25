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
                "width": 60,
                "height": 12,
                "text_template": """{storage_path}
{description}""",
                "template": """{
  "qrcode": {
    "type": "qrcode",
    "position": {          "x": 1,          "y": 1        },
    "width": 10,
    "height": 10
  },
  "name": {
        "type": "text",
        "position": {          "x": 12,          "y": 1        },
        "width": 47,
        "height": 3,
        "alignment": "left",
        "verticalAlignment": "middle",
        "fontSize": 13,
        "lineHeight": 1,
        "characterSpacing": 0,
        "dynamicFontSize": {          "min": 1,          "max": 20,          "fit": "horizontal"        }
  },
  "category": {
        "type": "text",
        "position": {          "x": 12,          "y": 4       },
        "width": 47,
        "height": 3,
        "rotate": 0,
        "alignment": "left",
        "verticalAlignment": "middle",
        "fontSize": 13,
        "lineHeight": 1,
        "characterSpacing": 0,
        "dynamicFontSize": {          "min": 1,          "max": 20,          "fit": "vertical"        }
  },
  "description": {
        "type": "text",
        "position": {          "x": 12,          "y": 7        },
        "width": 47,
        "height": 4.5,
        "alignment": "left",
        "verticalAlignment": "middle",
        "fontSize": 13,
        "lineHeight": 1,
        "characterSpacing": 0,
        "dynamicFontSize": {          "min": 1,          "max": 10,          "fit": "vertical"     }
  }
}""",
            },
            {
                "name": "Brother 90x38",
                "width": 90,
                "height": 38,
                "text_template": """{storage_path}

{description}""",
                "template": """{
  "qrcode": {
    "type": "qrcode",
    "position": {          "x": 1,          "y": 1        },
    "width": 36,
    "height": 36
  },
  "name": {
        "type": "text",
        "position": {          "x": 39,          "y": 1        },
        "width": 45,
        "height": 6,
        "alignment": "left",
        "verticalAlignment": "middle",
        "fontSize": 13,
        "lineHeight": 1,
        "characterSpacing": 0,
        "dynamicFontSize": {          "min": 1,          "max": 20,          "fit": "horizontal"        }
  },
  "category": {
        "type": "text",
        "position": {          "x": 39,          "y": 8        },
        "width": 45,
        "height": 6,
        "rotate": 0,
        "alignment": "left",
        "verticalAlignment": "middle",
        "fontSize": 13,
        "lineHeight": 1,
        "characterSpacing": 0,
        "dynamicFontSize": {          "min": 1,          "max": 20,          "fit": "vertical"        }
  },
  "description": {
        "type": "text",
        "position": {          "x": 39,          "y": 15        },
        "width": 45,
        "height": 22,
        "alignment": "left",
        "verticalAlignment": "middle",
        "fontSize": 13,
        "lineHeight": 1,
        "characterSpacing": 0,
        "dynamicFontSize": {          "min": 1,          "max": 10,          "fit": "vertical"     }
  }
}""",
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
