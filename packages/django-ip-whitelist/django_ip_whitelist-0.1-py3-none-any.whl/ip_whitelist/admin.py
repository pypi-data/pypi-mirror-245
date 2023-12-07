from django.contrib import admin
from import_export.resources import ModelResource

from .models import AllowedIP, AllowedIPRange
from .utils import ExportLogMixin


class AllowedIPResource(ModelResource):
    class Meta:
        model = AllowedIP
        fields = (
            "id",
            "owner",
            "address",
        )


@admin.register(AllowedIP)
class AllowedIPAdmin(ExportLogMixin, admin.ModelAdmin):
    resource_class = AllowedIPResource
    list_display = ("address", "owner")
    search_fields = (
        "owner",
        "address",
    )


class AllowedIPRangeResource(ModelResource):
    class Meta:
        model = AllowedIPRange
        fields = (
            "id",
            "owner",
            "range",
        )


@admin.register(AllowedIPRange)
class AllowedIPRangeAdmin(ExportLogMixin, admin.ModelAdmin):
    resource_class = AllowedIPRangeResource
    list_display = ("range", "owner")
    list_display = ("range", "owner")
    search_fields = (
        "owner",
        "range",
    )
