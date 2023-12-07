from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from import_export.admin import ExportMixin


def get_request_ips(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ips = x_forwarded_for.split(",")
        ips = map(str.strip, ips)
    else:
        ips = [request.META.get("REMOTE_ADDR")]

    return ips


class ExportLogMixin(ExportMixin):
    def get_export_queryset(self, request):
        """
        This is the closest we can get to the actual exporting (signal doesnt have the request information)
        """
        value = super().get_export_queryset(request)
        ids = ",".join(map(str, value.values_list("pk", flat=True)))
        LogEntry.user_action(
            ContentType.objects.get_for_model(self.model),
            message=f"Admin export: {self.model._meta.verbose_name}: [{ids}]",
            request=request,
        )
        return value
