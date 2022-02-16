from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from fpdf import FPDF
import base64


class LabelTemplate(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    width = models.IntegerField(blank=False, null=False, default=90, help_text="in mm")
    height = models.IntegerField(blank=False, null=False, default=38, help_text="in mm")
    base_pdf = models.TextField(editable=False)
    template = models.TextField(blank=False, null=False)
    text_template = models.TextField(
        blank=False,
        null=False,
        default="""{name}
{description}""",
    )


@receiver(pre_save, sender=LabelTemplate)
def set_base_pdf(sender, instance, **kwargs):
    # L is H*W, P is W*H
    fpdf = FPDF(
        orientation="L",
        unit="mm",
        format=(
            instance.height,
            instance.width,
        ),
    )
    fpdf.add_page()
    pdf = fpdf.output(dest="S")  # as byte string
    instance.base_pdf = f"data:application/pdf;base64,{base64.b64encode(pdf.encode('latin-1')).decode('UTF-8')}"
