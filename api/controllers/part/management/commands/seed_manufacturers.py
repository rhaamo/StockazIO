from os import path

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand

from controllers.manufacturer.models import Manufacturer


class Command(BaseCommand):
    help = """ Seed Manufacturers """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        print("Seeding Manufacturers...")
        with open("{0}/../setup-data/manufacturers/manufacturers.yaml".format(settings.BASE_DIR), "r") as stream:
            manufacturers = yaml.load(stream, Loader=yaml.FullLoader)

        for name in manufacturers:
            try:
                man = Manufacturer.objects.get(name=name)
                # also check for aliases
                if manufacturers[name]:
                    if "aliases" in manufacturers[name]:
                        aliases = [x.strip() for x in man.aliases]
                        for alias in manufacturers[name]["aliases"]:
                            if alias.strip() not in aliases:
                                aliases.append(alias.strip())
                        man.aliases = ", ".join(aliases)
                        man.save()
            except Manufacturer.DoesNotExist:
                man = Manufacturer(name=name)

                if manufacturers[name]:
                    if "logos" in manufacturers[name]:
                        logo = manufacturers[name]["logos"][0]  # take first
                        fi = open("{0}/../setup-data/manufacturers/images/{1}".format(settings.BASE_DIR, logo), "rb")
                        man.logo.save(path.basename(logo), fi, save=False)
                    if "datasheet_url" in manufacturers[name]:
                        man.datasheet_url = manufacturers[name]["datasheet_url"]
                man.save()

            except Manufacturer.MultipleObjectsReturned:
                print(f"WARNING: Multiple entries returned for {name!r}, skipping")
                continue
