from django.core.validators import ValidationError
from django.test import TestCase

from ip_whitelist.validators import validate_allowed_range_field


class ValidateAllowedRangeFieldTestCase(TestCase):
    def test_ip4_range(self):
        validate_allowed_range_field("192.168.1.1/32")

    def test_bad_address(self):
        with self.assertRaises(ValidationError):
            validate_allowed_range_field("256.123.1231.12")

    def test_bad_range(self):
        with self.assertRaises(ValidationError):
            validate_allowed_range_field("192.168.0.0/8")
