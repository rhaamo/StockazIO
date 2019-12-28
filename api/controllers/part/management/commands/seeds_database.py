from os import path

import yaml
import json
from django.conf import settings
from django.core.management.base import BaseCommand

from controllers.part.models import PartUnit, ParametersUnit
from controllers.footprints.models import Footprint, FootprintCategory
from controllers.categories.models import Category
from controllers.manufacturer.models import Manufacturer, ManufacturerLogo
from controllers.distributor.models import Distributor


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


def seed_categories():
    print("+++ 000 --- Seeding Categories")
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


def seed_parameters_unit():
    print("+++ 000 --- Seeding Parameters Units")
    with open("{0}/../setup-data/units.yaml".format(settings.BASE_DIR), "r") as stream:
        units = yaml.load(stream, Loader=yaml.FullLoader)

    for i in units:
        for ii in units[i]["prefixes"]:
            try:
                pu = ParametersUnit.objects.get(name=i, symbol=units[i]["symbol"], prefix=ii)
            except ParametersUnit.DoesNotExist:
                pu = ParametersUnit(name=i, symbol=units[i]["symbol"], prefix=ii)
                pu.save()
            except ParametersUnit.MultipleObjectsReturned:
                print(
                    f"WARNING: Multiple entries returned for name={i!r}, symbol={units[i]['symbol']!r}, prefix={ii!r}"
                )
                continue


def seed_manufacturers():
    print("+++ 000 --- Seeding Manufacturers")
    with open("{0}/../setup-data/manufacturers/manufacturers.yaml".format(settings.BASE_DIR), "r") as stream:
        manufacturers = yaml.load(stream, Loader=yaml.FullLoader)

    for name in manufacturers:
        try:
            man = Manufacturer.objects.get(name=name)
        except Manufacturer.DoesNotExist:
            man = Manufacturer(name=name)
            man.save()

            for logo in manufacturers[name]:
                f = ManufacturerLogo(manufacturer=man)
                fi = open("{0}/../setup-data/manufacturers/images/{1}".format(settings.BASE_DIR, logo), "rb")
                f.logo.save(path.basename(logo), fi, save=False)
                f.save()

        except Manufacturer.MultipleObjectsReturned:
            print(f"WARNING: Multiple entries returned for {name!r}, skipping")
            continue


def seed_distributors():
    print("+++ 000 --- Seeding Distributors")
    distributors = [
        ["Farnell element14", "http://farnell.com/"],
        ["Mouser Electronics", "http://www.mouser.fr/"],
        ["DigiKey Electronics", "https://www.digikey.com/"],
        ["TME", "https://www.tme.eu/"],
    ]
    for name, url in distributors:
        try:
            distributor = Distributor.objects.get(name=name, url=url)
        except Distributor.DoesNotExist:
            distributor = Distributor(name=name, url=url)
            distributor.save()
        except Distributor.MultipleObjectsReturned:
            print(f"WARNING: Multiple entries returned for {name!r}, {url!r}, skipping")
            continue


class Command(BaseCommand):
    help = """ 000 Initial seed """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        seed_part_units()
        seed_footprints()
        seed_categories()
        seed_parameters_unit()
        seed_manufacturers()
        seed_distributors()
