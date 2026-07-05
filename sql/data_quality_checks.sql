-- 02: Data quality checks

-- Purpose:
-- Identify data quality issues in the raw engineering deliverables dataset.

SET search_path TO engineering_data;

-- ============================================================
-- 1. BASIC ROW COUNT VALIDATION
-- ============================================================

SELECT 'fact_engineering_deliverables' AS table_name, COUNT(*) AS row_count FROM fact_engineering_deliverables
UNION ALL SELECT 'dim_project', COUNT(*) FROM dim_project
UNION ALL SELECT 'dim_discipline', COUNT(*) FROM dim_discipline
UNION ALL SELECT 'dim_document_type', COUNT(*) FROM dim_document_type
UNION ALL SELECT 'dim_status', COUNT(*) FROM dim_status
UNION ALL SELECT 'dim_engineer', COUNT(*) FROM dim_engineer
UNION ALL SELECT 'dim_equipment', COUNT(*) FROM dim_equipment
UNION ALL SELECT 'dim_date', COUNT(*) FROM dim_date;

-- ============================================================
-- 2. DATA QUALITY ISSUE ROWS
-- ============================================================
-- This view returns one row per deliverable per issue.
-- A single deliverable can appear more than once if it has multiple issues.

DROP VIEW IF EXISTS vw_data_quality_by_discipline;
DROP VIEW IF EXISTS vw_data_quality_by_project;
DROP VIEW IF EXISTS vw_data_quality_summary;
DROP VIEW IF EXISTS vw_data_quality_issue_rows;

CREATE OR REPLACE VIEW vw_data_quality_issue_rows AS
WITH
parameters AS (
    SELECT
        DATE '2026-07-04' AS reference_date,
        20 AS long_review_threshold_days
),
duplicate_documents AS (
    SELECT document_id
    FROM fact_engineering_deliverables
    WHERE document_id IS NOT NULL
    GROUP BY document_id
    HAVING COUNT(*) > 1
),
base AS (
    SELECT
        f.deliverable_id,
        f.project_id,
        f.document_id,
        f.document_title,
        f.discipline_id,
        f.document_type_id,
        f.equipment_id,
        f.responsible_engineer_id,
        f.status_id,
        f.revision_number,
        f.planned_submission_date,
        f.actual_submission_date,
        f.planned_approval_date,
        f.actual_approval_date,
        f.review_cycle_count,
        f.created_date,
        f.last_updated_date,
        f.comments,
        p.project_name,
        p.project_phase,
        p.project_status,
        d.discipline_name,
        dt.document_type_name,
        s.status_name,
        s.status_group,
        e.engineer_name,
        eq.equipment_tag,
        eq.equipment_type,
        eq.area,
        eq.system,
        eq.criticality,
        prm.reference_date,
        prm.long_review_threshold_days
    FROM fact_engineering_deliverables f
    CROSS JOIN parameters prm
    LEFT JOIN dim_project p
        ON f.project_id = p.project_id
    LEFT JOIN dim_discipline d
        ON f.discipline_id = d.discipline_id
    LEFT JOIN dim_document_type dt
        ON f.document_type_id = dt.document_type_id
    LEFT JOIN dim_status s
        ON f.status_id = s.status_id
    LEFT JOIN dim_engineer e
        ON f.responsible_engineer_id = e.responsible_engineer_id
    LEFT JOIN dim_equipment eq
        ON f.equipment_id = eq.equipment_id
)

-- Missing owner
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Missing Metadata' AS issue_category,
    'Missing Owner' AS issue_type,
    'High' AS severity,
    'Responsible engineer is missing.' AS issue_description
FROM base
WHERE NULLIF(TRIM(responsible_engineer_id), '') IS NULL

UNION ALL

-- Missing equipment
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Missing Metadata',
    'Missing Equipment',
    'Medium',
    'Equipment ID is missing in the deliverable record.'
FROM base
WHERE NULLIF(TRIM(equipment_id), '') IS NULL

UNION ALL

-- Missing discipline
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Missing Metadata',
    'Missing Discipline',
    'High',
    'Discipline ID is missing in the deliverable record.'
FROM base
WHERE NULLIF(TRIM(discipline_id), '') IS NULL

UNION ALL

-- Missing document type
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Missing Metadata',
    'Missing Document Type',
    'Medium',
    'Document type ID is missing in the deliverable record.'
FROM base
WHERE NULLIF(TRIM(document_type_id), '') IS NULL

UNION ALL

-- Missing project phase
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Missing Metadata',
    'Missing Project Phase',
    'Medium',
    'Project phase is missing in dim_project.'
FROM base
WHERE NULLIF(TRIM(project_phase), '') IS NULL

UNION ALL

-- Duplicate document ID
SELECT
    b.deliverable_id, b.document_id, b.project_id, b.project_name,
    b.discipline_id, b.discipline_name, b.document_type_id, b.document_type_name,
    b.equipment_id, b.equipment_tag, b.responsible_engineer_id, b.engineer_name,
    b.status_id, b.status_name,
    'Duplicate',
    'Duplicate Document ID',
    'High',
    'Document ID appears more than once in the fact table.'
FROM base b
INNER JOIN duplicate_documents dd
    ON b.document_id = dd.document_id

UNION ALL

-- Invalid status
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Reference Integrity',
    'Invalid Status',
    'High',
    'Status ID exists in the fact table but does not exist in dim_status.'
FROM base
WHERE NULLIF(TRIM(status_id), '') IS NOT NULL
  AND status_name IS NULL

UNION ALL

-- Invalid project reference
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Reference Integrity',
    'Invalid Project Reference',
    'High',
    'Project ID exists in the fact table but does not exist in dim_project.'
FROM base
WHERE NULLIF(TRIM(project_id), '') IS NOT NULL
  AND project_name IS NULL

UNION ALL

-- Invalid discipline reference
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Reference Integrity',
    'Invalid Discipline Reference',
    'High',
    'Discipline ID exists in the fact table but does not exist in dim_discipline.'
FROM base
WHERE NULLIF(TRIM(discipline_id), '') IS NOT NULL
  AND discipline_name IS NULL

UNION ALL

-- Invalid document type reference
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Reference Integrity',
    'Invalid Document Type Reference',
    'Medium',
    'Document type ID exists in the fact table but does not exist in dim_document_type.'
FROM base
WHERE NULLIF(TRIM(document_type_id), '') IS NOT NULL
  AND document_type_name IS NULL

UNION ALL

-- Invalid engineer reference
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Reference Integrity',
    'Invalid Engineer Reference',
    'High',
    'Responsible engineer ID exists in the fact table but does not exist in dim_engineer.'
FROM base
WHERE NULLIF(TRIM(responsible_engineer_id), '') IS NOT NULL
  AND engineer_name IS NULL

UNION ALL

-- Invalid equipment reference
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Reference Integrity',
    'Invalid Equipment Reference',
    'Medium',
    'Equipment ID exists in the fact table but does not exist in dim_equipment.'
FROM base
WHERE NULLIF(TRIM(equipment_id), '') IS NOT NULL
  AND equipment_tag IS NULL

UNION ALL

-- Invalid equipment criticality
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Invalid Value',
    'Invalid Equipment Criticality',
    'Medium',
    'Equipment criticality must be High, Medium, or Low.'
FROM base
WHERE equipment_id IS NOT NULL
  AND criticality IS NOT NULL
  AND criticality NOT IN ('High', 'Medium', 'Low')

UNION ALL

-- Invalid revision number
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Invalid Value',
    'Invalid Revision Number',
    'Medium',
    'Revision number must be between 0 and 5.'
FROM base
WHERE revision_number < 0
   OR revision_number > 5

UNION ALL

-- Planned submission after actual submission
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Invalid Date',
    'Planned Submission After Actual Submission',
    'High',
    'Planned submission date is later than actual submission date.'
FROM base
WHERE planned_submission_date IS NOT NULL
  AND actual_submission_date IS NOT NULL
  AND planned_submission_date > actual_submission_date

UNION ALL

-- Planned approval before planned submission
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Invalid Date',
    'Planned Approval Before Planned Submission',
    'Medium',
    'Planned approval date is earlier than planned submission date.'
FROM base
WHERE planned_submission_date IS NOT NULL
  AND planned_approval_date IS NOT NULL
  AND planned_approval_date < planned_submission_date

UNION ALL

-- Actual approval before actual submission
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Invalid Date',
    'Actual Approval Before Actual Submission',
    'High',
    'Actual approval date is earlier than actual submission date.'
FROM base
WHERE actual_submission_date IS NOT NULL
  AND actual_approval_date IS NOT NULL
  AND actual_approval_date < actual_submission_date

UNION ALL

-- Completed deliverable missing actual submission date
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Workflow Issue',
    'Completed Deliverable Missing Actual Submission Date',
    'High',
    'Approved or rejected deliverable is missing actual submission date.'
FROM base
WHERE status_name IN ('Approved', 'Rejected')
  AND actual_submission_date IS NULL

UNION ALL

-- Approved deliverable missing actual approval date
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Workflow Issue',
    'Approved Deliverable Missing Actual Approval Date',
    'High',
    'Approved deliverable is missing actual approval date.'
FROM base
WHERE status_name = 'Approved'
  AND actual_approval_date IS NULL

UNION ALL

-- Overdue deliverable
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Delay',
    'Overdue Deliverable',
    'Medium',
    'Deliverable is not closed and planned submission date is before the reference date.'
FROM base
WHERE status_name NOT IN ('Approved', 'Cancelled')
  AND planned_submission_date IS NOT NULL
  AND planned_submission_date < reference_date

UNION ALL

-- Long review cycle
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Workflow Issue',
    'Long Review Cycle',
    'Medium',
    'Deliverable has been under review for longer than the defined threshold.'
FROM base
WHERE status_name = 'Under Review'
  AND actual_submission_date IS NOT NULL
  AND (reference_date - actual_submission_date) > long_review_threshold_days

UNION ALL

-- Last updated before created date
SELECT
    deliverable_id, document_id, project_id, project_name,
    discipline_id, discipline_name, document_type_id, document_type_name,
    equipment_id, equipment_tag, responsible_engineer_id, engineer_name,
    status_id, status_name,
    'Invalid Date',
    'Last Updated Before Created Date',
    'Medium',
    'Last updated date is earlier than created date.'
FROM base
WHERE created_date IS NOT NULL
  AND last_updated_date IS NOT NULL
  AND last_updated_date < created_date;

-- ============================================================
-- 3. SUMMARY VIEWS
-- ============================================================

CREATE OR REPLACE VIEW vw_data_quality_summary AS
SELECT
    issue_category,
    issue_type,
    severity,
    COUNT(*) AS issue_count,
    COUNT(DISTINCT deliverable_id) AS affected_deliverables
FROM vw_data_quality_issue_rows
GROUP BY issue_category, issue_type, severity;

CREATE OR REPLACE VIEW vw_data_quality_by_project AS
SELECT
    project_id,
    project_name,
    issue_category,
    issue_type,
    severity,
    COUNT(*) AS issue_count,
    COUNT(DISTINCT deliverable_id) AS affected_deliverables
FROM vw_data_quality_issue_rows
GROUP BY project_id, project_name, issue_category, issue_type, severity;

CREATE OR REPLACE VIEW vw_data_quality_by_discipline AS
SELECT
    discipline_id,
    discipline_name,
    issue_category,
    issue_type,
    severity,
    COUNT(*) AS issue_count,
    COUNT(DISTINCT deliverable_id) AS affected_deliverables
FROM vw_data_quality_issue_rows
GROUP BY discipline_id, discipline_name, issue_category, issue_type, severity;

-- ============================================================
-- 4. QUICK CHECK QUERIES
-- ============================================================

SELECT
    issue_category,
    issue_type,
    severity,
    issue_count,
    affected_deliverables
FROM vw_data_quality_summary
ORDER BY issue_count DESC, issue_type;

SELECT
    COUNT(*) AS total_issue_rows,
    COUNT(DISTINCT deliverable_id) AS deliverables_with_at_least_one_issue
FROM vw_data_quality_issue_rows;

SELECT
    issue_type,
    COUNT(*) AS issue_count
FROM vw_data_quality_issue_rows
GROUP BY issue_type
ORDER BY issue_count DESC;
