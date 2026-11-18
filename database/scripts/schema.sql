
-- =====================================================
-- SSRMS: Secure Student Records Management System
-- BIT3360 Advanced Databases
-- =====================================================

-- TABLE 1: USERS
-- Stores login accounts and application roles.

CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY,

    username VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password_hash TEXT NOT NULL,

    role VARCHAR(20) NOT NULL,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_users PRIMARY KEY (user_id),

    CONSTRAINT uq_users_username UNIQUE (username),

    CONSTRAINT uq_users_email UNIQUE (email),

    CONSTRAINT chk_users_role
        CHECK (role IN ('administrator', 'lecturer', 'student'))
);


-- TABLE 2: STUDENTS
-- Stores academic information for student accounts.

CREATE TABLE students (
    student_id BIGINT GENERATED ALWAYS AS IDENTITY,

    user_id BIGINT NOT NULL,

    student_number VARCHAR(30) NOT NULL,

    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,

    programme VARCHAR(120) NOT NULL,

    year_of_study SMALLINT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_students PRIMARY KEY (student_id),

    CONSTRAINT uq_students_user UNIQUE (user_id),

    CONSTRAINT uq_students_number UNIQUE (student_number),

    CONSTRAINT fk_students_users
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_students_year
        CHECK (year_of_study BETWEEN 1 AND 8)
);
