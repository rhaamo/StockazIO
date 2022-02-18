import magic
from django.core.management.base import BaseCommand

from controllers.part.models import Part


class Command(BaseCommand):
    help = """
    If you had Part Files Attachment before the split in two file fields, use this command to convert everything.
    """

    def __init__(self, *args, **kwargs):
        BaseCommand.__init__(self, *args, **kwargs)
        self.target = None

    def handle(self, *args, **options):
        for part in Part.objects.all():
            part_attachments = part.part_attachments.all()
            if len(part_attachments) > 0:
                print(f"Processing attachments for #{part.id}: {part.name}")
                treated = 0
                for pa in part_attachments:
                    if not pa.file:
                        continue
                    mime_type = magic.from_buffer(pa.file.read(1024), mime=True)
                    if mime_type.startswith("image/"):
                        pa.picture = pa.file
                        pa.file_size = pa.file.size
                        pa.file_type = mime_type
                        pa.file = None
                        print(f"Part attachment #{pa.id} has been moved from file to picture")
                        pa.save()
                        treated += 1
                if not part.part_attachments.filter(picture_default=True):
                    pa = part.part_attachments.first()
                    pa.picture_default = True
                    pa.save()
                if treated == 0:
                    print("   > No attachment to handle.")
