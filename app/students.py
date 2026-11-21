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

@students_bp.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@role_required("administrator")
def edit_student(student_id):
    if request.method == "POST":
        student_number = request.form.get("student_number", "").strip()
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        programme = request.form.get("programme", "").strip()

        try:
            year_of_study = int(request.form.get("year_of_study", ""))

            if not all([
                student_number,
                first_name,
                last_name,
                programme
            ]):
                flash("All fields are required.", "error")
                return redirect(
                    url_for("students.edit_student", student_id=student_id)
                )

            if not 1 <= year_of_study <= 8:
                flash("Year of study must be between 1 and 8.", "error")
                return redirect(
                    url_for("students.edit_student", student_id=student_id)
                )

            connection = get_db_connection(role="administrator")

            with closing(connection):
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE students
                        SET
                            student_number = %s,
                            first_name = %s,
                            last_name = %s,
                            programme = %s,
                            year_of_study = %s
                        WHERE student_id = %s
                        RETURNING student_id
                        """,
                        (
                            student_number,
                            first_name,
                            last_name,
                            programme,
                            year_of_study,
                            student_id
                        )
                    )

                    updated_student = cursor.fetchone()

                connection.commit()

            if updated_student is None:
                flash("Student record not found.", "error")
                return redirect(url_for("students.list_students"))

            flash("Student record updated successfully.", "success")
            return redirect(url_for("students.list_students"))

        except ValueError:
            flash("Year of study must be a valid number.", "error")

        except Exception as error:
            print(f"Update student error: {error}")
            flash("Unable to update student record.", "error")

    # Retrieve the existing record for the edit form
    try:
        connection = get_db_connection(role="administrator")

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
                    WHERE student_id = %s
                    """,
                    (student_id,)
                )

                student = cursor.fetchone()

    except Exception as error:
        print(f"Retrieve student error: {error}")
        flash("Unable to retrieve student record.", "error")
        return redirect(url_for("students.list_students"))

    if student is None:
        flash("Student record not found.", "error")
        return redirect(url_for("students.list_students"))

    return render_template("edit_student.html", student=student)
@students_bp.route("/students/<int:student_id>/delete", methods=["POST"])
@role_required("administrator")
def delete_student(student_id):
    try:
        connection = get_db_connection(role="administrator")

        with closing(connection):
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM students
                    WHERE student_id = %s
                    RETURNING student_id
                    """,
                    (student_id,)
                )

                deleted_student = cursor.fetchone()

            connection.commit()

        if deleted_student is None:
            flash("Student record not found.", "error")
        else:
            flash("Student record deleted successfully.", "success")

    except Exception as error:
        print(f"Delete student error: {error}")
        flash("Unable to delete student record.", "error")

    return redirect(url_for("students.list_students"))