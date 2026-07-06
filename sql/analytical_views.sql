-- 03: Analytical views for Power BI

-- Purpose:
-- Create reusable analytical views for Power BI.

SET search_path TO engineering_data;


-- ============================================================
-- 1. DELIVERABLES OVERVIEW
-- ============================================================
-- One row per engineering deliverable.
-- This is the main view for the Power BI model.

DROP VIEW IF EXISTS vw_deliverables_overview;

CREATE OR REPLACE VIEW vw_deliverables_overview AS

WITH
parameters AS (
    SELECT
        DATE '2026-07-04' AS reference_date
),

issue_counts AS (
    SELECT
        deliverable_id,
        COUNT(*) AS data_quality_issue_count,
        COUNT(DISTINCT issue_type) AS distinct_data_quality_issue_count
    FROM vw_data_quality_issue_rows
    GROUP BY deliverable_id
)

SELECT
    f.deliverable_id,
    f.project_id,
    p.project_name,
    p.client,
    p.project_phase,
    p.project_manager,
    p.project_start_date,
    p.project_end_date,
    p.project_status,

    f.document_id,
    f.document_title,
    f.document_type_id,
    dt.document_type_name,

    f.discipline_id,
    d.discipline_name,

    f.equipment_id,
    eq.equipment_tag,
    eq.equipment_type,
    eq.area,
    eq.system,
    eq.criticality,

    f.responsible_engineer_id,
    e.engineer_name,
    e.role AS engineer_role,
    e.team AS engineer_team,
    e.location AS engineer_location,

    f.status_id,
    COALESCE(s.status_name, 'Invalid Status') AS status_name,
    COALESCE(s.status_group, 'Invalid Status') AS status_group,

    f.revision_number,
    f.review_cycle_count,

    f.planned_submission_date,
    f.actual_submission_date,
    f.planned_approval_date,
    f.actual_approval_date,
    f.created_date,
    f.last_updated_date,
    f.comments,

    prm.reference_date,

    CASE
        WHEN s.status_name = 'Approved' THEN TRUE
        ELSE FALSE
    END AS is_completed,

    CASE
        WHEN s.status_name IN ('Approved', 'Cancelled') THEN TRUE
        ELSE FALSE
    END AS is_closed,

    CASE
        WHEN s.status_name IN (
            'Not Started',
            'In Progress',
            'Under Review',
            'Rejected',
            'Delayed'
        ) THEN TRUE
        ELSE FALSE
    END AS is_pending,

    CASE
        WHEN s.status_name IN ('Not Started', 'In Progress', 'Delayed')
             AND f.actual_submission_date IS NULL
             AND f.planned_submission_date < prm.reference_date
        THEN TRUE

        WHEN s.status_name IN ('Under Review', 'Rejected')
             AND f.actual_approval_date IS NULL
             AND f.planned_approval_date < prm.reference_date
        THEN TRUE

        ELSE FALSE
    END AS is_overdue,

    CASE
        WHEN f.actual_submission_date IS NOT NULL
             AND f.planned_submission_date IS NOT NULL
        THEN f.actual_submission_date - f.planned_submission_date
        ELSE NULL
    END AS submission_variance_days,

    CASE
        WHEN f.actual_submission_date IS NOT NULL
             AND f.planned_submission_date IS NOT NULL
             AND f.actual_submission_date > f.planned_submission_date
        THEN f.actual_submission_date - f.planned_submission_date
        ELSE 0
    END AS late_submission_days,

    CASE
        WHEN s.status_name IN ('Not Started', 'In Progress', 'Delayed')
             AND f.actual_submission_date IS NULL
             AND f.planned_submission_date < prm.reference_date
        THEN prm.reference_date - f.planned_submission_date

        WHEN s.status_name IN ('Under Review', 'Rejected')
             AND f.actual_approval_date IS NULL
             AND f.planned_approval_date < prm.reference_date
        THEN prm.reference_date - f.planned_approval_date

        ELSE 0
    END AS current_overdue_days,

    CASE
        WHEN f.actual_submission_date IS NOT NULL
             AND f.actual_approval_date IS NOT NULL
        THEN f.actual_approval_date - f.actual_submission_date
        ELSE NULL
    END AS review_cycle_days,

    CASE
        WHEN s.status_name = 'Under Review'
             AND f.actual_submission_date IS NOT NULL
             AND f.actual_submission_date <= prm.reference_date
        THEN prm.reference_date - f.actual_submission_date
        ELSE NULL
    END AS days_under_review,

    COALESCE(ic.data_quality_issue_count, 0) AS data_quality_issue_count,
    COALESCE(ic.distinct_data_quality_issue_count, 0) AS distinct_data_quality_issue_count,

    CASE
        WHEN COALESCE(ic.data_quality_issue_count, 0) > 0 THEN TRUE
        ELSE FALSE
    END AS has_data_quality_issue

FROM fact_engineering_deliverables f

CROSS JOIN parameters prm

LEFT JOIN dim_project p
    ON f.project_id = p.project_id

LEFT JOIN dim_document_type dt
    ON f.document_type_id = dt.document_type_id

LEFT JOIN dim_discipline d
    ON f.discipline_id = d.discipline_id

LEFT JOIN dim_equipment eq
    ON f.equipment_id = eq.equipment_id

LEFT JOIN dim_engineer e
    ON f.responsible_engineer_id = e.responsible_engineer_id

LEFT JOIN dim_status s
    ON f.status_id = s.status_id

LEFT JOIN issue_counts ic
    ON f.deliverable_id = ic.deliverable_id;


-- ============================================================
-- 2. PROJECT PROGRESS
-- ============================================================
-- Aggregated project-level progress for dashboard cards and charts.

DROP VIEW IF EXISTS vw_project_progress;

CREATE OR REPLACE VIEW vw_project_progress AS

SELECT
    project_id,
    project_name,
    client,
    project_phase,
    project_manager,
    project_status,

    COUNT(*) AS total_deliverables,

    SUM(
        CASE WHEN is_completed = TRUE THEN 1 ELSE 0 END
    ) AS completed_deliverables,

    SUM(
        CASE WHEN is_pending = TRUE THEN 1 ELSE 0 END
    ) AS pending_deliverables,

    SUM(
        CASE WHEN is_overdue = TRUE THEN 1 ELSE 0 END
    ) AS overdue_deliverables,

    ROUND(
        SUM(CASE WHEN is_completed = TRUE THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(*), 0),
        4
    ) AS completion_rate,

    ROUND(
        SUM(CASE WHEN is_overdue = TRUE THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(*), 0),
        4
    ) AS overdue_rate,

    SUM(data_quality_issue_count) AS total_data_quality_issues,

    SUM(
        CASE WHEN has_data_quality_issue = TRUE THEN 1 ELSE 0 END
    ) AS deliverables_with_quality_issues,

    ROUND(
        SUM(CASE WHEN has_data_quality_issue = TRUE THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(*), 0),
        4
    ) AS deliverables_with_quality_issues_rate,

    ROUND(
        AVG(current_overdue_days)::NUMERIC,
        2
    ) AS average_current_overdue_days,

    ROUND(
        AVG(review_cycle_days)::NUMERIC,
        2
    ) AS average_review_cycle_days

FROM vw_deliverables_overview

GROUP BY
    project_id,
    project_name,
    client,
    project_phase,
    project_manager,
    project_status;


-- ============================================================
-- 3. REVIEW CYCLE PERFORMANCE
-- ============================================================
-- Analysis by document type and discipline.

DROP VIEW IF EXISTS vw_review_cycle_performance;

CREATE OR REPLACE VIEW vw_review_cycle_performance AS

SELECT
    discipline_id,
    discipline_name,
    document_type_id,
    document_type_name,

    COUNT(*) AS total_deliverables,

    SUM(
        CASE WHEN status_name = 'Under Review' THEN 1 ELSE 0 END
    ) AS deliverables_under_review,

    SUM(
        CASE WHEN status_name = 'Rejected' THEN 1 ELSE 0 END
    ) AS rejected_deliverables,

    SUM(
        CASE WHEN is_overdue = TRUE THEN 1 ELSE 0 END
    ) AS overdue_deliverables,

    ROUND(
        AVG(review_cycle_count)::NUMERIC,
        2
    ) AS average_review_cycle_count,

    ROUND(
        AVG(review_cycle_days)::NUMERIC,
        2
    ) AS average_review_cycle_days,

    ROUND(
        AVG(days_under_review)::NUMERIC,
        2
    ) AS average_days_under_review,

    ROUND(
        AVG(current_overdue_days)::NUMERIC,
        2
    ) AS average_current_overdue_days

FROM vw_deliverables_overview

GROUP BY
    discipline_id,
    discipline_name,
    document_type_id,
    document_type_name;


-- ============================================================
-- 4. ENGINEERING WORKFLOW STATUS
-- ============================================================
-- Status-level view for workflow bottleneck analysis.

DROP VIEW IF EXISTS vw_engineering_workflow_status;

CREATE OR REPLACE VIEW vw_engineering_workflow_status AS

SELECT
    status_id,
    status_name,
    status_group,
    project_id,
    project_name,
    discipline_id,
    discipline_name,

    COUNT(*) AS total_deliverables,

    SUM(
        CASE WHEN is_overdue = TRUE THEN 1 ELSE 0 END
    ) AS overdue_deliverables,

    SUM(
        CASE WHEN has_data_quality_issue = TRUE THEN 1 ELSE 0 END
    ) AS deliverables_with_quality_issues,

    ROUND(
        AVG(current_overdue_days)::NUMERIC,
        2
    ) AS average_current_overdue_days,

    ROUND(
        AVG(days_under_review)::NUMERIC,
        2
    ) AS average_days_under_review

FROM vw_deliverables_overview

GROUP BY
    status_id,
    status_name,
    status_group,
    project_id,
    project_name,
    discipline_id,
    discipline_name;


-- ============================================================
-- 5. IMPROVEMENT OPPORTUNITIES
-- ============================================================
-- Prioritizes improvement opportunities based on issue volume and severity.

DROP VIEW IF EXISTS vw_improvement_opportunities;

CREATE OR REPLACE VIEW vw_improvement_opportunities AS

SELECT
    issue_category,
    issue_type,
    severity,

    COUNT(*) AS issue_count,
    COUNT(DISTINCT deliverable_id) AS affected_deliverables,

    COUNT(DISTINCT project_id) AS affected_projects,
    COUNT(DISTINCT discipline_id) AS affected_disciplines,

    CASE
        WHEN severity = 'High' THEN 3
        WHEN severity = 'Medium' THEN 2
        WHEN severity = 'Low' THEN 1
        ELSE 1
    END AS severity_weight,

    COUNT(*) *
    CASE
        WHEN severity = 'High' THEN 3
        WHEN severity = 'Medium' THEN 2
        WHEN severity = 'Low' THEN 1
        ELSE 1
    END AS priority_score,

    CASE
        WHEN issue_type IN (
            'Missing Owner',
            'Missing Equipment',
            'Missing Equipment Tag',
            'Missing Discipline',
            'Missing Document Type',
            'Missing Project Phase'
        )
        THEN 'Define mandatory metadata fields and ownership routines.'

        WHEN issue_type IN (
            'Duplicate Document ID',
            'Missing Document ID'
        )
        THEN 'Standardize document ID naming conventions and validation rules.'

        WHEN issue_type IN (
            'Invalid Status',
            'Invalid Project Reference',
            'Invalid Engineer Reference',
            'Invalid Equipment Reference',
            'Invalid Discipline Reference',
            'Invalid Document Type Reference'
        )
        THEN 'Create reference data validation before reporting publication.'

        WHEN issue_type IN (
            'Planned Submission After Actual Submission',
            'Planned Approval Before Planned Submission',
            'Actual Approval Before Actual Submission',
            'Last Updated Before Created Date'
        )
        THEN 'Implement date validation rules in the source tracking process.'

        WHEN issue_type IN (
            'Approved Deliverable Missing Actual Approval Date',
            'Completed Deliverable Missing Actual Submission Date',
            'Long Review Cycle'
        )
        THEN 'Improve workflow governance, review SLAs, and approval tracking.'

        WHEN issue_type = 'Overdue Deliverable'
        THEN 'Monitor overdue deliverables weekly and assign clear follow-up ownership.'

        ELSE 'Review business rule and define corrective action.'
    END AS recommended_action

FROM vw_data_quality_issue_rows

GROUP BY
    issue_category,
    issue_type,
    severity;


-- ============================================================
-- 6. QUICK VALIDATION QUERIES
-- ============================================================
-- Run these after executing the script.

SELECT
    COUNT(*) AS total_deliverables
FROM vw_deliverables_overview;

SELECT
    project_name,
    total_deliverables,
    completed_deliverables,
    pending_deliverables,
    overdue_deliverables,
    completion_rate,
    overdue_rate
FROM vw_project_progress
ORDER BY overdue_deliverables DESC;

SELECT
    issue_type,
    severity,
    issue_count,
    affected_deliverables,
    priority_score,
    recommended_action
FROM vw_improvement_opportunities
ORDER BY priority_score DESC;
