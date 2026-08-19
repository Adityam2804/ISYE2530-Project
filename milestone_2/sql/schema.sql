-- ============================================================
-- Milestone 2 Relational Schema
-- ============================================================
--
-- STUDENT FILE
--
-- Your task is to translate the relational structure proposed
-- in Milestone 1 into SQLite CREATE TABLE statements.
--
-- You do NOT write Python database-creation code.
-- src/database.py will read and execute this file for you.
--
-- Before writing this file:
-- 1. Review feasibility_preview.md from Milestone 1.
-- 2. Decide which entities/tables you actually need.
-- 3. Identify a primary key for each table.
-- 4. Identify relationships between tables.
-- 5. Make sure table names exactly match the dictionary returned
--    by split_into_tables().
--
-- SQLite types you will commonly use:
--
-- TEXT       names, identifiers, categories, ISO date strings
-- INTEGER    counts, whole numbers, integer IDs
-- REAL       decimal numeric values
--
-- Do not store every field as TEXT without a reason.
-- ============================================================

PRAGMA foreign_keys = ON;


-- ============================================================
-- STUDENT TASK 3A — First table
-- ============================================================
--
-- Example SHAPE only:
--
-- CREATE TABLE entities (
--     entity_id TEXT PRIMARY KEY,
--     category TEXT
-- );
--
-- Replace with YOUR table.


-- STUDENT SQL HERE



-- ============================================================
-- STUDENT TASK 3B — Second table
-- ============================================================
--
-- Example SHAPE only:
--
-- CREATE TABLE events (
--     event_id TEXT PRIMARY KEY,
--     entity_id TEXT NOT NULL,
--     event_date TEXT,
--     numeric_value REAL,
--
--     FOREIGN KEY (entity_id)
--         REFERENCES entities(entity_id)
-- );
--
-- Replace with YOUR table.
--
-- Notice:
-- - primary key uniquely identifies a row
-- - foreign key links this table to another table
-- - NOT NULL is used only when the value is truly required


-- STUDENT SQL HERE



-- ============================================================
-- STUDENT TASK 3C — Additional tables, if approved/needed
-- ============================================================
--
-- Add additional CREATE TABLE statements below.
--
-- Keep the schema understandable.
-- More tables are NOT automatically better.

