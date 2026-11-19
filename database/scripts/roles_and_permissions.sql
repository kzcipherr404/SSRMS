-- =====================================================
-- SSRMS: Secure Student Records Management System
-- BIT3360 Advanced Databases
-- Task 3 & Task 4: Roles and Permissions
-- =====================================================


-- =====================================================
-- TASK 3: CREATE LOGIN ROLES
-- =====================================================

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ssrms_admin') THEN
        CREATE ROLE ssrms_admin
            LOGIN
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            NOREPLICATION;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ssrms_lecturer') THEN
        CREATE ROLE ssrms_lecturer
            LOGIN
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            NOREPLICATION;
    END IF;

    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'ssrms_student') THEN
        CREATE ROLE ssrms_student
            LOGIN
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            NOREPLICATION;
    END IF;
END
$$;


-- =====================================================
-- TASK 4: DATABASE AND SCHEMA PERMISSIONS
-- =====================================================

GRANT CONNECT ON DATABASE ssrms_db
TO ssrms_admin, ssrms_lecturer, ssrms_student;

GRANT USAGE ON SCHEMA public
TO ssrms_admin, ssrms_lecturer, ssrms_student;


-- =====================================================
-- TASK 4: TABLE-LEVEL PERMISSIONS
-- =====================================================

-- Administrator: Full access to student records
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE students
TO ssrms_admin;


-- Lecturer: Can view and add student records
GRANT SELECT, INSERT
ON TABLE students
TO ssrms_lecturer;


-- Student: Can view student records
-- Row-Level Security will restrict which records they see
GRANT SELECT
ON TABLE students
TO ssrms_student;


-- =====================================================
-- TASK 4: ENABLE ROW-LEVEL SECURITY
-- =====================================================

ALTER TABLE students ENABLE ROW LEVEL SECURITY;


-- =====================================================
-- ADMINISTRATOR POLICIES
-- =====================================================

CREATE POLICY admin_select_students
ON students
FOR SELECT
TO ssrms_admin
USING (true);


CREATE POLICY admin_insert_students
ON students
FOR INSERT
TO ssrms_admin
WITH CHECK (true);


CREATE POLICY admin_update_students
ON students
FOR UPDATE
TO ssrms_admin
USING (true)
WITH CHECK (true);


CREATE POLICY admin_delete_students
ON students
FOR DELETE
TO ssrms_admin
USING (true);


-- =====================================================
-- LECTURER POLICIES
-- =====================================================

CREATE POLICY lecturer_select_students
ON students
FOR SELECT
TO ssrms_lecturer
USING (true);


CREATE POLICY lecturer_insert_students
ON students
FOR INSERT
TO ssrms_lecturer
WITH CHECK (true);


-- =====================================================
-- STUDENT POLICY
-- =====================================================

CREATE POLICY student_select_own_record
ON students
FOR SELECT
TO ssrms_student
USING (
    user_id = current_setting('ssrms.current_user_id', true)::BIGINT
);


-- =====================================================
-- END OF ROLES AND PERMISSIONS SCRIPT
-- =====================================================