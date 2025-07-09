from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect
# from django.core.exceptions import PermissionDenied

class ManagerRequiredMixin(AccessMixin):
    """
    Verify that the current user is authenticated and is a manager.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_manager:
            # 403 Forbidden error
            # raise PermissionDenied("You do not have permission to access this page.")
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)