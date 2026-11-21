import unittest

from app import create_app
from app.security import role_required


class RBACTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True

        # Temporary test route
        @self.app.route("/admin-test")
        @role_required("administrator")
        def admin_test():
            return "Administrator access granted"

        self.client = self.app.test_client()

    def test_unauthenticated_user_is_redirected(self):
        response = self.client.get("/admin-test")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_student_cannot_access_admin_route(self):
        with self.client.session_transaction() as session:
            session["user_id"] = 4
            session["username"] = "student01"
            session["role"] = "student"

        response = self.client.get("/admin-test")

        self.assertEqual(response.status_code, 403)

    def test_administrator_can_access_admin_route(self):
        with self.client.session_transaction() as session:
            session["user_id"] = 1
            session["username"] = "admin01"
            session["role"] = "administrator"

        response = self.client.get("/admin-test")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.decode(),
            "Administrator access granted"
        )


if __name__ == "__main__":
    unittest.main()