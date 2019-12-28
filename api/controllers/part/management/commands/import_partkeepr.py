import os
import csv
from django.core.management.base import BaseCommand, CommandError

from controllers.part.models import Part, PartUnit
from controllers.footprints.models import Footprint, FootprintCategory
from controllers.categories.models import Category
from controllers.storage.models import StorageCategory, StorageLocation


class Command(BaseCommand):
    help = """
    Import from partkeepr "Custom Export" CSV *WITH* a header, as following:
    CSV Format:
    name, description, comment, stockLevel, minStockLevel, status, needsReview, partCondition, productionRemarks,
    internalPartNumber, category.name, category.categoryPath, footprint.name, footprint.category.name, partUnit.name,
    storageLocation.name, storageLocation.category.name
    """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str)

    def get_csv_file(self, filename):
        if filename.startswith("~"):
            return os.path.expanduser(filename)
        return filename

    def handle(self, *args, **options):
        if "file" not in options:
            raise CommandError("You need to give a --file= to consume")
        file_path = self.get_csv_file(options["file"])
        print(f"Importing from {file_path!r}")
        count = 0
        count_imported = 0
        try:
            with open(file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                for row in csv_reader:
                    # Get or create part unit
                    if row["partUnit.name"] == "null":
                        part_unit = None
                    else:
                        part_unit, _ = PartUnit.objects.get_or_create(name=row["partUnit.name"])
                    # Get Category if possible
                    try:
                        category = Category.objects.get(name=row["category.name"])
                        if row["category.categoryPath"].replace("➤", "->") != category.__str__():
                            category = None
                    except Category.MultipleObjectsReturned:
                        category = None
                    # Get footprint category if possible
                    try:
                        footprint_category = FootprintCategory.objects.get(name=row["footprint.category.name"])
                    except FootprintCategory.DoesNotExist:
                        footprint_category = None
                    except FootprintCategory.MultipleObjectsReturned:
                        footprint_category = None
                    # Try to get footprint
                    try:
                        footprint = Footprint.objects.get(name=row["footprint.name"], footprint=footprint_category)
                    except Footprint.DoesNotExist:
                        footprint = None
                    except Footprint.MultipleObjectsReturned:
                        footprint = None
                    # Get storage category if possible
                    try:
                        storage_category = StorageCategory.objects.get(name=row["storageLocation.category.name"])
                        if row["storageLocation.category.name"].replace("➤", "->") != storage_category.__str__():
                            storage_category = None
                    except StorageCategory.DoesNotExist:
                        storage_category = None
                    except StorageCategory.MultipleObjectsReturned:
                        storage_category = None
                    # Get storage location if possible
                    try:
                        storage = StorageLocation.objects.get(
                            name=row["storageLocation.name"], category=storage_category
                        )
                    except StorageLocation.DoesNotExist:
                        storage = None
                    except StorageLocation.MultipleObjectsReturned:
                        storage = None
                    # Create part if does not exist
                    part, _ = Part.objects.get_or_create(
                        name=row["name"],
                        description=row["description"],
                        comment=row["comment"],
                        stock_qty=row["stockLevel"],
                        stock_qty_min=row["minStockLevel"],
                        status=row["status"],
                        needs_review=False if row["needsReview"] == "false" else True,
                        condition=row["partCondition"],
                        production_remarks=row["productionRemarks"],
                        internal_part_number=row["internalPartNumber"],
                        category=category,
                        footprint=footprint,
                        part_unit=part_unit,
                        storage=storage,
                    )
                    count = count + 1
                    count_imported = count_imported + 1

        except FileNotFoundError:
            raise CommandError(f"File {file_path!r} does not exist.")

        print(f"Imported {count_imported} of {count} lines")
