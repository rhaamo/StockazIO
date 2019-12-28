from os import path

import yaml
from django.conf import settings
from django.core.management.base import BaseCommand

from controllers.part.models import PartUnit  # , ParametersUnit
from controllers.footprints.models import Footprint, FootprintCategory

# from vendoring.models import Distributor, Manufacturer, ManufacturerLogo


def seed_part_units():
    print("+++ 000 --- Seeding Part Units")
    units = [["Centimeters", "cm"], ["Pieces", "pcs"]]
    for u in units:
        try:
            _ = PartUnit.objects.get(name=u[0], short_name=u[1])
        except PartUnit.DoesNotExist:
            unit = PartUnit(name=u[0], short_name=u[1])
            unit.save()
        except PartUnit.MultipleObjectsReturned:
            print(f"WARNING: Multiple entries returned for {u!r}")


def seed_footprints():
    print("+++ 000 --- Seeding Footprints")
    with open("{0}/../setup-data/footprints/footprints.yaml".format(settings.BASE_DIR), "r") as stream:
        z = yaml.load(stream, Loader=yaml.FullLoader)

    for i in z:
        try:
            cat = FootprintCategory.objects.get(name=i)
        except FootprintCategory.DoesNotExist:
            cat = FootprintCategory(name=i)
            cat.save()
        except FootprintCategory.MultipleObjectsReturned:
            print(f"WARNING: Multiple entries returned for category: {i!r}, skipped")
            continue

        for ii in z[i]:
            try:
                f = Footprint.objects.get(name=ii, footprint=cat, description=z[i][ii]["description"])
            except Footprint.DoesNotExist:
                f = Footprint(name=ii, footprint=cat, description=z[i][ii]["description"])
            except Footprint.MultipleObjectsReturned:
                print(f"WARNING: Multiple entries returned for footprint: {ii!r}, skipping")
                continue
            if "image" in z[i][ii]:
                fi = open("{0}/../setup-data/footprints/{1}".format(settings.BASE_DIR, z[i][ii]["image"]), "rb")
                f.picture.save(path.basename(z[i][ii]["image"]), fi, save=False)
            f.save()


def seed_parameters_unit():
    print("+++ 000 --- Seeding Parameters Units")
    with open("{0}/../setup-data/units.yaml".format(settings.BASE_DIR), "r") as stream:
        units = yaml.load(stream, Loader=yaml.FullLoader)

    for i in units:
        for ii in units[i]["prefixes"]:
            a = ParametersUnit(name=i, symbol=units[i]["symbol"], prefix=ii)
            a.save()


def seed_manufacturers():
    print("+++ 000 --- Seeding Manufacturers")
    with open("{0}/../setup-data/manufacturers/manufacturers.yaml".format(settings.BASE_DIR), "r") as stream:
        manufacturers = yaml.load(stream, Loader=yaml.FullLoader)

    for name in manufacturers:
        man = Manufacturer(name=name)
        man.save()

        for logo in manufacturers[name]:
            f = ManufacturerLogo(manufacturer=man)
            fi = open("{0}/setup-data/manufacturers/images/{1}".format(settings.BASE_DIR, logo), "rb")
            f.logo.save(path.basename(logo), fi, save=False)
            f.save()


def seed_distributors():
    print("+++ 000 --- Seeding Distributors")
    distributors = [
        ["Farnell element14", "http://farnell.com/"],
        ["Mouser Electronics", "http://www.mouser.fr/"],
        ["DigiKey Electronics", "https://www.digikey.com/"],
        ["TME", "https://www.tme.eu/"],
    ]
    for d in distributors:
        distributor = Distributor(name=d[0], url=d[1])
        distributor.save()


class Command(BaseCommand):
    help = """ 000 Initial seed """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        seed_part_units()
        seed_footprints()
        # seed_parameters_unit()
        # seed_manufacturers()
        # seed_distributors()
