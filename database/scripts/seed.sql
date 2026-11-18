
-- =====================================================
-- SSRMS: Secure Student Records Management System
-- BIT3360 Advanced Databases
-- =====================================================

BEGIN;

-- =====================================================
-- 1. INSERT USER ACCOUNTS
-- Passwords are stored as Werkzeug-compatible PBKDF2 hashes.
-- All accounts are fictional demonstration accounts.
-- =====================================================

INSERT INTO users (
    username,
    email,
    password_hash,
    role
)
VALUES

(
    'admin01',
    'admin01@ssrms.example',
    'pbkdf2:sha256:600000$93316537b8c4bcdc$502af75f066073fa5cdb8567e6639d0865acef656078d417e65a521e66d3f4a6',
    'administrator'
),

(
    'lecturer01',
    'lecturer01@ssrms.example',
    'pbkdf2:sha256:600000$cd6e5637f677b896$fbb6a4b8798cb66a0e03ed7f62b0ebac413bbf9297ce8ab3f2fb75917c313e43',
    'lecturer'
),

(
    'lecturer02',
    'lecturer02@ssrms.example',
    'pbkdf2:sha256:600000$5c0d5440fb21b68b$524f5e3612b56d7d4b9cc95e8ffdb9f070186967ef0d1fa8dbcec7c7a522f4b0',
    'lecturer'
),

(
    'student01',
    'student01@ssrms.example',
    'pbkdf2:sha256:600000$8584867b84d307de$eede9062f197a3afa73fd87e06735388e946e128c7b3abe40b565f52fedd6f0d',
    'student'
),

(
    'student02',
    'student02@ssrms.example',
    'pbkdf2:sha256:600000$de1899d0e96091a5$dd4f71c6738229b4703eb9b76e94b5b88208dc45cb692e7fb95ab1afa5dffa7f',
    'student'
),

(
    'student03',
    'student03@ssrms.example',
    'pbkdf2:sha256:600000$b1682888ffe95c91$38664492692b9300a8f4967a3b4031049b6fb8b41f147d3b01ff410c1686e5e9',
    'student'
),

(
    'student04',
    'student04@ssrms.example',
    'pbkdf2:sha256:600000$dfef14a5092fa53a$a5e55425eb7e931aca70c6e0d2a1419a8dd157e21e32c1d4ebcd724879b513ba',
    'student'
)

ON CONFLICT (username) DO NOTHING;


-- =====================================================
-- 2. INSERT STUDENT ACADEMIC RECORDS
-- Link each student to their existing user account.
-- =====================================================

INSERT INTO students (
    user_id,
    student_number,
    first_name,
    last_name,
    programme,
    year_of_study
)

SELECT
    u.user_id,
    sample.student_number,
    sample.first_name,
    sample.last_name,
    sample.programme,
    sample.year_of_study

FROM (
    VALUES
    (
        'student01',
        'SSRMS2026001',
        'Chanda',
        'Phiri',
        'Cyber Security',
        3
    ),
    (
        'student02',
        'SSRMS2026002',
        'Natasha',
        'Banda',
        'Software Engineering',
        2
    ),
    (
        'student03',
        'SSRMS2026003',
        'Mwila',
        'Tembo',
        'Information Technology',
        3
    ),
    (
        'student04',
        'SSRMS2026004',
        'Daniel',
        'Zulu',
        'Computer Science',
        1
    )

) AS sample (
    username,
    student_number,
    first_name,
    last_name,
    programme,
    year_of_study
)

JOIN users u
    ON u.username = sample.username
    AND u.role = 'student'

ON CONFLICT (student_number) DO NOTHING;


COMMIT;

-- =====================================================
-- END OF SSRMS SAMPLE DATA
-- =====================================================
