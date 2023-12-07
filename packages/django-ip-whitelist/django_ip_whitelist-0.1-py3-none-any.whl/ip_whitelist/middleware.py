import ipaddress
import logging

from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import HttpResponseRedirect, reverse
from django.urls import reverse_lazy
from django.urls.resolvers import RegexPattern, URLResolver

from tests import settings

from .models import AllowedIP, AllowedIPRange
from .utils import get_request_ips

logger = logging.getLogger(__name__)


class IPWhiteListMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        if self.allowed_path(request):
            response = self.get_response(request)
        else:
            response = HttpResponseRedirect(settings.LOGIN_URL)
        return response

    @staticmethod
    def is_allowed(ips, allowed_ips, allowed_ranges):
        allowed = False
        for ip_str in ips:
            if ip_str in allowed_ips:
                allowed = True
                break

            ip = ipaddress.ip_address(ip_str)

            for allowed_range in allowed_ranges:
                try:
                    network = ipaddress.ip_network(allowed_range)
                except ValueError as e:
                    logger.warning(
                        "Failed to parse specific network address: {}".format(
                            "".join(e.args)
                        )
                    )
                    continue

                if ip in network:
                    allowed = True
                    break

            if allowed:
                break

        return allowed

    def process_request(self, request):
        allowed_ips = set(settings.WHITELIST_IPS)
        cached_allowed_ips = cache.get("allowed_ips", None)
        if cached_allowed_ips is None:
            db_allowed_ips = AllowedIP.objects.values_list("address", flat=True)
            cache.set("allowed_ips", list(db_allowed_ips))
            cached_allowed_ips = cache.get("allowed_ips")
        allowed_ips.update(cached_allowed_ips)

        allowed_ranges = set(settings.WHITELIST_IP_RANGES)
        cached_allowed_ranges = cache.get("allowed_ranges", None)
        if cached_allowed_ranges is None:
            db_allowed_ranges = AllowedIPRange.objects.values_list("range", flat=True)
            cache.set("allowed_ranges", list(db_allowed_ranges))
            cached_allowed_ranges = cache.get("allowed_ranges")
        allowed_ranges.update(cached_allowed_ranges)

        ips = get_request_ips(request)

        # Check cached and settings ips.
        allowed = self.is_allowed(
            ips=ips, allowed_ips=allowed_ips, allowed_ranges=allowed_ranges
        )
        setattr(request, "ip_allowed", allowed)

    def allowed_path(self, request):
        allowed = getattr(request, "ip_allowed", False)
        external_flatpage = getattr(request, "external_flatpage", False)

        resolver = URLResolver(
            pattern=RegexPattern("^/"), urlconf_name=settings.ROOT_URLCONF
        )
        resolved_request = resolver.resolve(request.path)
        namespace = "{}:{}".format(
            resolved_request.namespace, resolved_request.url_name
        )

        if external_flatpage:
            return True

        if not request.user.is_authenticated and not allowed:
            for path in settings.NO_AUTH_OUTSIDE_IP_ALLOWED_PATHS:
                if path == namespace:
                    return True

            return False

        if request.user.is_authenticated and not allowed:
            if request.path.startswith(reverse("admin:index")):
                raise PermissionDenied

        return True
