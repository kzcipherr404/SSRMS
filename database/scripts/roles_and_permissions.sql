-- =====================================================
-- SSRMS: Secure Student Records Management System
-- BIT3360 Advanced Databases
-- =====================================================

-- Create administrator login role
CREATE ROLE ssrms_admin
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION;


-- Create lecturer login role
CREATE ROLE ssrms_lecturer
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION;


-- Create student login role
CREATE ROLE ssrms_student
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    NOREPLICATION;