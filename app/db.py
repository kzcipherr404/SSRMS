import psycopg
from config import Config


def get_db_connection(role="auth", user_id=None):
    """
    Create a PostgreSQL connection using a restricted application role.

    Supported roles:
        auth
        administrator
        lecturer
        student
    """

    role_config = {
        "auth": (
            Config.DB_AUTH_USER,
            Config.DB_AUTH_PASSWORD
        ),
        "administrator": (
            Config.DB_ADMIN_USER,
            Config.DB_ADMIN_PASSWORD
        ),
        "lecturer": (
            Config.DB_LECTURER_USER,
            Config.DB_LECTURER_PASSWORD
        ),
        "student": (
            Config.DB_STUDENT_USER,
            Config.DB_STUDENT_PASSWORD
        )
    }

    if role not in role_config:
        raise ValueError("Invalid database role")

    db_user, db_password = role_config[role]

    connection = psycopg.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        dbname=Config.DB_NAME,
        user=db_user,
        password=db_password
    )

    # Set the authenticated student's ID for PostgreSQL RLS.
    if role == "student":
        if user_id is None:
            connection.close()
            raise ValueError("Student user_id is required")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT set_config('ssrms.current_user_id', %s, false)",
                (str(user_id),)
            )

    return connection