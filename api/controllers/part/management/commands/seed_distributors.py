from django.core.management.base import BaseCommand

from controllers.distributor.models import Distributor


class Command(BaseCommand):
    help = """ Seed Distributors """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        print("Seeding Distributors...")
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
