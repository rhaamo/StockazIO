import csv
from os import path

from django.conf import settings
from django.core.management.base import BaseCommand

from controllers.footprints.models import Footprint, FootprintCategory


def save_footprint(fp_realname, db_fp_category, fp_description, picture):
    print(f"Saving {fp_realname!r} in category {db_fp_category.name!r} with description {fp_description!r}")
    try:
        f = Footprint.objects.get(name=fp_realname, category=db_fp_category, description=fp_description)
    except Footprint.DoesNotExist:
        f = Footprint(name=fp_realname, category=db_fp_category, description=fp_description)
    except Footprint.MultipleObjectsReturned:
        print(f"WARNING: Multiple entries returned for footprint: {fp_realname!r}, skipping")
        return
    if len(picture) > 0:
        fi = open("{0}/../setup-data/footprints/images/{1}".format(settings.BASE_DIR, picture), "rb")
        f.picture.save(path.basename(picture), fi, save=False)
    f.save()


class Command(BaseCommand):
    help = """ Seed Footprints """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
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
        print("Seeding Footprints...")
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
