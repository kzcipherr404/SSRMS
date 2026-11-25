# Secure Student Records Management System (SSRMS)

**Course:** BIT3360 – Advanced Databases  
**Topic:** Database Security  
**Institution:** Zambia University College of Technology

SSRMS is a Flask web application backed by PostgreSQL. It demonstrates authentication, role-based access control, PostgreSQL permissions, row-level security (RLS), and parameterised SQL queries using fictional student records.

> This is an academic prototype. Run it locally and use fictional data only. It is not intended for production use.

## 1. Technology requirements

Install the following on Windows:

- Python 3.10 or later
- PostgreSQL for Windows
- pgAdmin 4 (or PostgreSQL SQL Shell / `psql`)
- Git (if cloning the repository)

Docker is **not required**. PostgreSQL runs as a local Windows service.

Download PostgreSQL: <https://www.postgresql.org/download/windows/>

During PostgreSQL installation, include the server, pgAdmin 4, and command-line tools if offered. Keep the default port `5432` unless it is already in use.

## 2. Get the project

If you are using Git:

```powershell
git clone <GROUP_REPOSITORY_URL>
cd SSRMS
```

Alternatively, extract the supplied project ZIP, then open PowerShell in the extracted `SSRMS` folder.

Do not reuse another developer's `.venv` folder. Create your own environment by following the next step.

## 3. Create a Python virtual environment

From the project root (`SSRMS`), run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `pip` reports an encoding error while reading `requirements.txt`, save that file as UTF-8 and retry the installation.

## 4. Start PostgreSQL and create the database

1. Open **Services** in Windows and confirm that the PostgreSQL service is running. You can also connect through pgAdmin 4.
2. Connect to the local PostgreSQL server using the administrator account created during installation:
   - Host: `localhost`
   - Port: `5432`
   - Maintenance database: `postgres`
   - Username: `postgres`
   - Password: the password you chose during installation
3. Open the Query Tool in pgAdmin (or connect using `psql`) and create the project database:

```sql
CREATE DATABASE ssrms_db;
```

If the database already exists, do not create it again.

## 5. Create the database tables, roles and sample data

Run the SQL files from the project root, in this order:

1. `database/scripts/schema.sql`
2. `database/scripts/roles_and_permissions.sql`
3. `database/scripts/seed.sql`

In pgAdmin, select the `ssrms_db` database, open **Tools → Query Tool**, open each file, and execute it in the order above.

You can also use PowerShell with `psql` (adjust the PostgreSQL installation path if necessary):

```powershell
psql -U postgres -d ssrms_db -f database/scripts/schema.sql
psql -U postgres -d ssrms_db -f database/scripts/roles_and_permissions.sql
psql -U postgres -d ssrms_db -f database/scripts/seed.sql
```

The SQL scripts create the `users` and `students` tables, database demonstration roles, permissions and fictional sample records. The permissions script enables RLS on `students`.

### Important: configure the authentication database role

The Flask application uses four PostgreSQL connection configurations: authentication, administrator, lecturer and student. The supplied permissions script creates the administrator, lecturer and student roles. It does **not** create the separate authentication role.

Create the authentication login role using the exact username you will put in `DB_AUTH_USER` in your local `.env` file. For example (replace the placeholder values):

```sql
CREATE ROLE ssrms_auth
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION
    PASSWORD 'REPLACE_WITH_A_STRONG_LOCAL_PASSWORD';

GRANT CONNECT ON DATABASE ssrms_db TO ssrms_auth;
GRANT USAGE ON SCHEMA public TO ssrms_auth;
GRANT SELECT ON TABLE users TO ssrms_auth;
```

If you choose a different role name, use that same name in `DB_AUTH_USER`.

The three demonstration roles created by `roles_and_permissions.sql` also need login passwords. Set a separate local password for each role. For example:

```sql
ALTER ROLE ssrms_admin WITH PASSWORD 'REPLACE_WITH_ADMIN_PASSWORD';
ALTER ROLE ssrms_lecturer WITH PASSWORD 'REPLACE_WITH_LECTURER_PASSWORD';
ALTER ROLE ssrms_student WITH PASSWORD 'REPLACE_WITH_STUDENT_PASSWORD';
```

Use the corresponding values in your local `.env` file. Do not use the PostgreSQL `postgres` superuser as the application's runtime account.

## 6. Configure environment variables

Create a file named `.env` in the project root (the same folder as `app.py` and `config.py`).

Add the following configuration, then replace every placeholder with your own local credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ssrms_db

DB_AUTH_USER=ssrms_auth
DB_AUTH_PASSWORD=replace_with_auth_password

DB_ADMIN_USER=ssrms_admin
DB_ADMIN_PASSWORD=replace_with_admin_password

DB_LECTURER_USER=ssrms_lecturer
DB_LECTURER_PASSWORD=replace_with_lecturer_password

DB_STUDENT_USER=ssrms_student
DB_STUDENT_PASSWORD=replace_with_student_password

SECRET_KEY=replace_with_a_long_random_secret
```

Generate a random Flask secret key with:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SECRET_KEY`.

**Never commit `.env` to GitHub.** It contains local database credentials and the Flask session secret. The repository's `.gitignore` is configured to ignore it.

## 7. Run the application

Make sure:

- The virtual environment is activated.
- PostgreSQL is running.
- The `ssrms_db` database and SQL objects have been created.
- The `.env` values match the PostgreSQL roles and passwords.

Start the Flask application:

```powershell
python app.py
```

When Flask starts successfully, open this address in your browser:

<http://127.0.0.1:5000>

To stop the development server, press `CTRL+C` in the terminal.

## 8. Application roles

| Application role | View student records | Add records | Update records | Delete records |
|---|---|---|---|---|
| Administrator | All records | Yes | Yes | Yes |
| Lecturer | All records | Yes | No | No |
| Student | Own record only | No | No | No |

The application checks permissions on the server. PostgreSQL permissions provide a second layer of enforcement, and RLS restricts student-role queries to the authenticated student's own record.

## 9. Sample application accounts

The seed script inserts fictional demonstration accounts with usernames:

- `admin01`
- `lecturer01`
- `lecturer02`
- `student01`
- `student02`
- `student03`
- `student04`

The seed file stores password hashes, not readable passwords. Use the demonstration passwords supplied separately by the project group. If no password list was supplied, ask the project maintainer to provide or reset the demo credentials; do not assume the PostgreSQL role passwords are the same as application login passwords.

## 10. Run the security tests

With the virtual environment active, run:

```powershell
python -m unittest discover -s tests -v
```

The current test suite checks basic Flask role-based access control, including unauthenticated access, a student attempting to access an administrator-only route, and an administrator accessing that route.

For the database demonstration, also test the PostgreSQL grants and RLS policies using the separate database roles. Capture evidence of both permitted and rejected operations for the assignment presentation.

## 11. Troubleshooting

| Problem | What to check |
|---|---|
| `Connection refused` | Confirm the PostgreSQL Windows service is running and `DB_HOST` / `DB_PORT` are correct. |
| `password authentication failed` | Confirm each `.env` username and password matches its PostgreSQL login role. |
| `role ... does not exist` | Run the roles SQL script and create the separate authentication role described above. |
| `permission denied for table users` | Confirm the authentication role has `SELECT` on `users`. |
| `permission denied for table students` | Check that the correct application database role has the required table privileges. |
| `database "ssrms_db" does not exist` | Create the database before running the SQL scripts. |
| `psql` is not recognised | Use SQL Shell from the Start menu or add PostgreSQL's `bin` directory to PATH. |
| Port `5432` is already in use | Check for another PostgreSQL instance and update `DB_PORT` if you intentionally use a different port. |
| Flask cannot start | Activate `.venv`, install `requirements.txt`, and check the terminal traceback. |

## 12. Security and handling rules

- Use fictional student data only.
- Never commit `.env`, passwords, secret keys, virtual environments or Python cache files.
- Do not run Flask using the PostgreSQL superuser.
- Use parameterised SQL queries for user-supplied values.
- Keep application-level role checks on the server; hiding interface buttons is not sufficient.
- Keep the prototype local unless the group agrees on a safe deployment plan.

## 13. Project structure

```text
SSRMS/
├── app/
│   ├── static/
│   │   └── css/
│   ├── templates/
│   ├── __init__.py
│   ├── audit.py
│   ├── auth.py
│   ├── db.py
│   ├── security.py
│   └── students.py
├── database/
│   └── scripts/
│       ├── roles_and_permissions.sql
│       ├── schema.sql
│       └── seed.sql
├── tests/
│   └── test_security.py
├── .env
├── .gitignore
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

## 14. Further project documentation

- `ARCHITECTURE.md` – system layers, request flow and role model.
- `NATIVE_POSTGRESQL_SETUP.md` – PostgreSQL installation and configuration on Windows.
- `PHASES.md` – development phases, deliverables and exit criteria.
- `CONTRIBUTION_GUIDE.md` – Git branching and group collaboration workflow.
