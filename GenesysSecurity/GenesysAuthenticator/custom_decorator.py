from functools import wraps
from django.http import HttpResponseForbidden


def designation_required(*allowed_designations):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_designation = getattr(request.user, 'designation', None)
            print(f"User Designation: {user_designation}")

            if user_designation in allowed_designations:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You do not have permission to access this page.")

        return _wrapped_view

    return decorator
