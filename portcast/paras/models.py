# Third Party Stuff
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

# portcast Stuff
from portcast.base.models import TimeStampedUUIDModel


# Create your models here.
class Paragraph(TimeStampedUUIDModel):
    para_content = models.TextField(_("Paragraph Content"), blank=False, null=False)

    class Meta:
        verbose_name = _("paragraph")
        verbose_name_plural = _("paragraphs")
        ordering = ("-created_at",)


class Dictionary(TimeStampedUUIDModel):
    word = models.CharField(
        _("word"), max_length=250, null=False, blank=False, unique=True
    )
    frequency = models.PositiveBigIntegerField(_("frequency"), default=0)
    phonetics = models.JSONField(_("phonetics"), default=dict)
    meanings = models.JSONField(_("meanings"), default=dict)
    license = models.JSONField(_("license"), default=dict)
    source_urls = ArrayField(
        models.TextField(null=False, blank=False),
        verbose_name=_("source urls"),
        blank=True,
        default=list,
    )

    class Meta:
        verbose_name = _("dictionary")
        verbose_name_plural = _("dictionary")
        ordering = ("-frequency",)
