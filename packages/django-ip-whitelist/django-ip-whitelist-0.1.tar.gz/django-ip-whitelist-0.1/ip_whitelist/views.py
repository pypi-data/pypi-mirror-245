from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.views import View
from sendfile import sendfile

from .storage import private_storage


class PrivateFileView(View):
    def get(self, request, path):
        # fmt:off
        deleted_attachments = (
            LogEntry.objects.filter(
                content_type=ContentType.objects.get_for_model(self),
                action_flag=3,
            )
        )
        # fmt:on

        if request.user.is_authenticated and path not in deleted_attachments:
            fs_path = private_storage.path(path)
            LogEntry.user_action(
                request.user, f"Private file access: {path}", request=request
            )
            return sendfile(request, fs_path, attachment=True)

        raise PermissionDenied
