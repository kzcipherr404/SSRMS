from contextlib import closing

from flask import (
    Blueprint,
    session,
    render_template,
    flash,
    redirect,
    url_for,
    request
)

from app.db import get_db_connection
from app.security import role_required


students_bp = Blueprint("students", __name__)


# =====================================================
# VIEW STUDENT RECORDS
# =====================================================

@students_bp.route("/students")
@role_required("administrator", "lecturer", "student")
def list_students():

    role = session.get("role")
    user_id = session.get("user_id")

    try:
        if role == "student":
            connection = get_db_connection(
                role="student",
                user_id=user_id
            )
        else:
            connection = get_db_connection(role=role)

        with closing(connection):
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        student_id,
                        student_number,
                        first_name,
                        last_name,
                        programme,
                        year_of_study
                    FROM students
                    ORDER BY student_id
                    """
                )

                students = cursor.fetchall()

    except Exception as error:
        print(f"Student records error: {error}")

        flash(
            "Unable to retrieve student records.",
            "error"
        )

        return redirect(url_for("auth.dashboard"))

    return render_template(
        "students.html",
        students=students,
        role=role
    )


# =====================================================
# ADD STUDENT RECORD
# =====================================================

@students_bp.route("/students/add", methods=["GET", "POST"])
@role_required("administrator", "lecturer")
def add_student():

    if request.method == "POST":

        try:
            user_id = int(request.form.get("user_id", ""))
            student_number = request.form.get(
                "student_number", ""
            ).strip()

            first_name = request.form.get(
                "first_name", ""
            ).strip()

            last_name = request.form.get(
                "last_name", ""
            ).strip()

            programme = request.form.get(
                "programme", ""
            ).strip()

            year_of_study = int(
                request.form.get("year_of_study", "")
            )

            # Validate required fields
            if not all([
                student_number,
                first_name,
                last_name,
                programme
            ]):
                flash(
                    "All fields are required.",
                    "error"
                )

                return redirect(
                    url_for("students.add_student")
                )

            # Validate year of study
            if not 1 <= year_of_study <= 8:
                flash(
                    "Year of study must be between 1 and 8.",
                    "error"
                )

                return redirect(
                    url_for("students.add_student")
                )

            role = session.get("role")

            connection = get_db_connection(role=role)

            with closing(connection):
                with connection.cursor() as cursor:

                    # Parameterized SQL query
                    cursor.execute(
                        """
                        INSERT INTO students (
                            user_id,
                            student_number,
                            first_name,
                            last_name,
                            programme,
                            year_of_study
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING student_id
                        """,
                        (
                            user_id,
                            student_number,
                            first_name,
                            last_name,
                            programme,
                            year_of_study
                        )
                    )

                    student_id = cursor.fetchone()[0]
                    connection.commit()

            flash(
                f"Student record #{student_id} added successfully.",
                "success"
            )

            return redirect(
                url_for("students.list_students")
            )

        except ValueError:
            flash(
                "Enter valid numeric values for User ID and year.",
                "error"
            )

        except Exception as error:
            print(f"Add student error: {error}")

            flash(
                "Unable to add student. Check the account ID and student number.",
                "error"
            )

    return render_template("add_student.html")