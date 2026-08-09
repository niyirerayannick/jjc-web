"""Dashboard access decorators."""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def dashboard_required(view_func):
    """Require login and dashboard access."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        profile = getattr(request.user, 'profile', None)
        if not profile or not (profile.has_dashboard_access() or request.user.is_staff):
            messages.error(request, 'You do not have access to the dashboard.')
            return redirect('core:home')
        return view_func(request, *args, **kwargs)
    return wrapper


def can_manage(area):
    """Require ability to manage a specific area."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f'/accounts/login/?next={request.path}')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            profile = getattr(request.user, 'profile', None)
            if not profile or not profile.can_manage(area):
                messages.error(request, 'You do not have permission for this action.')
                return redirect('dashboard:home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
