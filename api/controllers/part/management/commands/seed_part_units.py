from django.core.management.base import BaseCommand
from controllers.part.models import PartUnit


class Command(BaseCommand):
    help = """ Seed Part Units """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        print("Seeding Part Units...")
        units = [["Centimeters", "cm"], ["Pieces", "pcs"]]
        for u in units:
            try:
                _ = PartUnit.objects.get(name=u[0], short_name=u[1])
            except PartUnit.DoesNotExist:
                unit = PartUnit(name=u[0], short_name=u[1])
                unit.save()
            except PartUnit.MultipleObjectsReturned:
                print(f"WARNING: Multiple entries returned for {u!r}")
