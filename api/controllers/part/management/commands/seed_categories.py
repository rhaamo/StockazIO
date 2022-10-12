import json

from django.conf import settings
from django.core.management.base import BaseCommand

from controllers.categories.models import Category


class Command(BaseCommand):
    help = """ Seed Categories """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        print("Seeding Categories...")
        with open("{0}/../setup-data/categories.json".format(settings.BASE_DIR), "r") as stream:
            root_category = json.load(stream)

        # create root category
        try:
            rc = Category.objects.get(name=root_category["name"])
        except Category.DoesNotExist:
            rc = Category(name=root_category["name"])
            rc.save()
        except Category.MultipleObjectsReturned:
            print(f"WARNING: Multiple entries returned for root category {root_category['name']!r}")
            print("Cannot continue")
            return

        def walk_childrens(cat, parent=None, level=0):
            for child in cat["children"]:
                # try to get (children) category
                try:
                    cc = Category.objects.get(name=child["name"], parent=parent)
                except Category.DoesNotExist:
                    cc = Category(name=child["name"], parent=parent)
                    cc.save()
                if "children" in child:
                    walk_childrens(child, parent=cc, level=level + 1)

        walk_childrens(root_category, parent=rc, level=0)
