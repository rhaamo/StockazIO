from os import path

import yaml
import json
from django.conf import settings
from django.core.management.base import BaseCommand
import csv

from controllers.part.models import PartUnit, ParametersUnit
from controllers.footprints.models import Footprint, FootprintCategory
from controllers.categories.models import Category
from controllers.manufacturer.models import Manufacturer
from controllers.distributor.models import Distributor
from controllers.labeltemplate.models import LabelTemplate


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


def save_footprint(fp_realname, db_fp_category, fp_description, picture):
    print(f"Saving {fp_realname!r} in category {db_fp_category.name!r} with description {fp_description!r}")
    try:
        f = Footprint.objects.get(name=fp_realname, footprint=db_fp_category, description=fp_description)
    except Footprint.DoesNotExist:
        f = Footprint(name=fp_realname, footprint=db_fp_category, description=fp_description)
    except Footprint.MultipleObjectsReturned:
        print(f"WARNING: Multiple entries returned for footprint: {fp_realname!r}, skipping")
        return
    if len(picture) > 0:
        fi = open("{0}/../setup-data/footprints/images/{1}".format(settings.BASE_DIR, picture), "rb")
        f.picture.save(path.basename(picture), fi, save=False)
    f.save()


def seed_footprints():
    """
    CSV Format:
        delimiter: ;
        colums names, mandatory:
            - cat
            - name
            - size
            - wideness
            - multiple
            - catname
            - realname
            - description
            - picture
            - notes
            - categorydescription
        catname, realname and description can uses python {format}, with the following columns names: cat, name, wideness (and size if multiple=yes)
        multiple will uses the size column, split on ',', and create one footprint per size
        categorydescription is the category description, can uses {format} with same columns as catname and realname with description too
    """
    print("+++ 000 --- Seeding Footprints")
    with open("{0}/../setup-data/footprints/footprints.csv".format(settings.BASE_DIR), "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=";")
        for row in csv_reader:
            print(f"ROW: {row!r}")
            # Columns available for subst in catname, realname and description
            cols = dict(cat=row["cat"], name=row["name"], wideness=row["wideness"])

            # Footprint category
            footprint_category_name = row["catname"].format(**cols)
            fpcols = cols
            fpcols["description"] = row["description"]
            fpcols["size"] = row["size"]
            footprint_category_description = row["categorydescription"].format(**fpcols)
            # Fetch or create FootprintCategory
            try:
                db_footprint_category = FootprintCategory.objects.get(name=footprint_category_name)
            except FootprintCategory.DoesNotExist:
                db_footprint_category = FootprintCategory(
                    name=footprint_category_name, description=footprint_category_description
                )
                db_footprint_category.save()
            except FootprintCategory.MultipleObjectsReturned:
                print(f"WARNING: Multiple entries returned for category: {footprint_category_name!r}, skipped")
                continue

            # Footprints
            if row["multiple"].strip() == "yes":
                for size in row["size"].split(","):
                    cols_available = cols
                    cols_available["size"] = size
                    footprint_realname = row["realname"].format(**cols_available)
                    footprint_description = row["description"].format(**cols_available)
                    # Fetch or create Footprint
                    save_footprint(footprint_realname, db_footprint_category, footprint_description, row["picture"])
            else:
                footprint_realname = row["realname"].format(**cols)
                footprint_description = row["description"].format(**cols)
                save_footprint(footprint_realname, db_footprint_category, footprint_description, row["picture"])


def seed_footprints2():
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
        try:
            pu = ParametersUnit.objects.get(name=i, symbol=units[i]["symbol"])
        except ParametersUnit.DoesNotExist:
            pu = ParametersUnit(name=i, symbol=units[i]["symbol"])
            pu.save()
        except ParametersUnit.MultipleObjectsReturned:
            print(f"WARNING: Multiple entries returned for name={i!r}, symbol={units[i]['symbol']!r}")
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


def seed_distributors():
    print("+++ 000 --- Seeding Distributors")
    distributors = [
        ["Farnell element14", "http://farnell.com/", "http://www.farnell.com/datasheets/{_}.pdf"],
        ["Mouser Electronics", "http://www.mouser.com/", ""],
        ["DigiKey Electronics", "https://www.digikey.com/", ""],
        ["TME", "https://www.tme.eu/", ""],
        ["Arrow", "https://www.arrow.com/", ""],
        ["UtSource", "https://www.utsource.net/", ""],
        ["LCSC Electronics", "https://lcsc.com/", ""],
    ]
    for name, url, datasheet_url in distributors:
        try:
            distributor = Distributor.objects.get(name=name, url=url)
        except Distributor.DoesNotExist:
            distributor = Distributor(name=name, url=url, datasheet_url=datasheet_url)
            distributor.save()
        except Distributor.MultipleObjectsReturned:
            print(f"WARNING: Multiple entries returned for {name!r}, {url!r}, skipping")
            continue


def seed_label_templates():
    print("+++ 000 --- Seeding Label Templates")
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
        seed_label_templates()
