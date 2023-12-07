from django.core.cache import cache
from django.core.validators import validate_ipv46_address
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_allowed_range_field


class AllowedIP(models.Model):
    owner = models.CharField(_("Eigenaar"), max_length=255, null=False, blank=False)
    address = models.CharField(
        _("Address"),
        max_length=45,
        unique=True,
        null=False,
        blank=False,
        validators=(validate_ipv46_address,),
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        cache.delete("allowed_ips")
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    class Meta:
        verbose_name = "IP whitelist - adres"
        verbose_name_plural = "IP whitelist - adressen"

    def __str__(self):
        return "{} {}".format(self.address, self.owner)


class AllowedIPRange(models.Model):
    owner = models.CharField(_("Eigenaar"), max_length=255, null=False, blank=False)
    range = models.CharField(
        _("Range"),
        max_length=49,
        unique=True,
        null=False,
        blank=False,
        validators=(validate_allowed_range_field,),
    )

    class Meta:
        verbose_name = "IP whitelist - adres reeks"
        verbose_name_plural = "IP whitelist - reeksen"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        cache.delete("allowed_ranges")
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    def __str__(self):
        return "{} {}".format(self.range, self.owner)
