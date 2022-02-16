from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """ Launch all database seeds """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    # noinspection PyAttributeOutsideInit
    def handle(self, *args, **options):
        call_command("seed_part_units")
        call_command("seed_footprints")
        call_command("seed_categories")
        call_command("seed_parameters_unit")
        call_command("seed_manufacturers")
        call_command("seed_distributors")
        call_command("seed_label_templates")
