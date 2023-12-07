import ipaddress
import logging

from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def validate_allowed_range_field(value):
    try:
        ipaddress.IPv4Network(value)
    except (ValueError, AssertionError) as e:
        logger.info(f"Failed parsing value as ipv4 address: {e}")

        try:
            ipaddress.IPv6Network(value)
        except (ValueError, AssertionError):
            raise ValidationError(
                _("Enter a valid IPv4 or IPv6 address range in CIDR notation"),
                code="invalid",
            )
