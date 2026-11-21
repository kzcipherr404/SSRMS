from werkzeug.security import check_password_hash
from app.db import get_db_connection
from flask import Blueprint, render_template, request, redirect, url_for, flash, session


def authenticate_user(username, password):
    """
    Authenticate a user using their username and password.

    Returns user information if authentication succeeds.
    Returns None if authentication fails.
    """

    with get_db_connection() as connection:
        with connection.cursor() as cursor:

            # Parameterized query to retrieve the user
            cursor.execute(
                """
                SELECT
                    user_id,
                    username,
                    email,
                    password_hash,
                    role,
                    is_active
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            user = cursor.fetchone()

    # User does not exist
    if user is None:
        return None

    user_id, username, email, password_hash, role, is_active = user

    # Reject inactive accounts
    if not is_active:
        return None

    # Verify the submitted password against the stored hash
    if not check_password_hash(password_hash, password):
        return None

    # Return only necessary user information
    return {
        "user_id": user_id,
        "username": username,
        "email": email,
        "role": role
    }

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.
    """

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = authenticate_user(username, password)

        if user:

            # Clear any previous session data
            session.clear()

            # Store authenticated user information
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            flash("Login successful.", "success")

            return redirect(url_for("auth.dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@auth_bp.route("/dashboard")
def dashboard():
    """
    Display the dashboard to authenticated users.
    """

    if "user_id" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.login"))

    return f"""
        <h1>Welcome, {session['username']}!</h1>
        <p>Your role: {session['role']}</p>
        <a href="{url_for('auth.logout')}">Logout</a>
    """


@auth_bp.route("/logout")
def logout():
    """
    Log out the current user.
    """

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))