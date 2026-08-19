-- ============================================================
-- Milestone 2 Required SQL Checks
-- ============================================================
--
-- STUDENT FILE
--
-- Complete Q1-Q5 using the tables YOU created.
--
-- These are integrity/relational checks, not Milestone 3
-- decision analysis.
--
-- Keep the numbered Q1-Q5 comments exactly as written.
-- End each SQL query with a semicolon.
-- ============================================================


-- Q1. Show the row count for each major table.
--
-- TASK:
-- Report counts for your main relational tables.
--
-- Helpful pattern:
--
-- SELECT 'table_a' AS table_name, COUNT(*) AS row_count
-- FROM table_a
-- UNION ALL
-- SELECT 'table_b', COUNT(*)
-- FROM table_b;
--
-- STUDENT SQL BELOW:



-- Q2. Check whether the primary identifier of one major table contains duplicates.
--
-- TASK:
-- Choose one table and verify its intended primary identifier
-- does not appear more than once.
--
-- Helpful pattern:
--
-- SELECT entity_id, COUNT(*) AS occurrence_count
-- FROM entities
-- GROUP BY entity_id
-- HAVING COUNT(*) > 1;
--
-- A correct result may return ZERO rows.
--
-- STUDENT SQL BELOW:



-- Q3. Use a JOIN between at least two project tables and return a meaningful result.
--
-- TASK:
-- Demonstrate that the relationship between two tables works.
--
-- Helpful pattern:
--
-- SELECT ...
-- FROM table_a AS a
-- JOIN table_b AS b
--     ON a.key = b.key
-- LIMIT 20;
--
-- STUDENT SQL BELOW:



-- Q4. Use GROUP BY and an aggregate function to summarize the data.
--
-- TASK:
-- Use COUNT, SUM, AVG, MIN, or MAX with GROUP BY.
--
-- This should show that the relational database can support
-- a useful summary.
--
-- STUDENT SQL BELOW:



-- Q5. Write one dataset-specific integrity or data-quality query.
--
-- TASK:
-- Check one condition that is especially important for YOUR
-- cleaned database.
--
-- Examples of ideas:
-- - detail rows pointing to missing parent records
-- - impossible ranges that should have been removed
-- - missing values in a field required by your project
-- - duplicate combinations that should be unique
--
-- Do not copy an example unless it matches your project.
--
-- STUDENT SQL BELOW:

