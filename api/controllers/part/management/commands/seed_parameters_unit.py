import yaml
from django.core.management.base import BaseCommand
from controllers.part.models import ParametersUnit
from django.conf import settings


class Command(BaseCommand):
    help = """ Seed Parameters Units """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        print("Seeding Parameters Units...")
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
