from functools import wraps
from flask import session, redirect, url_for, flash, abort


def role_required(*allowed_roles):
    """
    Restrict access to users with specific roles.

    Usage:
        @role_required("administrator")
    """

    def decorator(view_function):

        @wraps(view_function)
        def wrapper(*args, **kwargs):

            # Require authentication
            if "user_id" not in session:
                flash("Please log in first.", "error")
                return redirect(url_for("auth.login"))

            # Check user's role
            if session.get("role") not in allowed_roles:
                abort(403)

            return view_function(*args, **kwargs)

        return wrapper

    return decorator