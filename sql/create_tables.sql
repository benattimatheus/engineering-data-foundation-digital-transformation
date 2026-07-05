-- Database: PostgreSQL
-- 01

CREATE SCHEMA IF NOT EXISTS engineering_data;

SET search_path TO engineering_data;

DROP TABLE IF EXISTS fact_engineering_deliverables;
DROP TABLE IF EXISTS dim_project;
DROP TABLE IF EXISTS dim_discipline;
DROP TABLE IF EXISTS dim_document_type;
DROP TABLE IF EXISTS dim_status;
DROP TABLE IF EXISTS dim_engineer;
DROP TABLE IF EXISTS dim_equipment;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_project (
    project_id          VARCHAR(20),
    project_name        VARCHAR(150),
    client              VARCHAR(100),
    project_phase       VARCHAR(50),
    project_manager     VARCHAR(100),
    project_start_date  DATE,
    project_end_date    DATE,
    project_status      VARCHAR(50)
);

CREATE TABLE dim_discipline (
    discipline_id    VARCHAR(20),
    discipline_name  VARCHAR(100)
);

CREATE TABLE dim_document_type (
    document_type_id    VARCHAR(20),
    document_type_name  VARCHAR(100)
);

CREATE TABLE dim_status (
    status_id     VARCHAR(20),
    status_name   VARCHAR(100),
    status_group  VARCHAR(50)
);

CREATE TABLE dim_engineer (
    responsible_engineer_id  VARCHAR(20),
    engineer_name            VARCHAR(100),
    role                     VARCHAR(100),
    discipline_id            VARCHAR(20),
    team                     VARCHAR(100),
    location                 VARCHAR(100)
);

CREATE TABLE dim_equipment (
    equipment_id    VARCHAR(20),
    equipment_tag   VARCHAR(50),
    equipment_type  VARCHAR(100),
    area            VARCHAR(100),
    system          VARCHAR(100),
    criticality     VARCHAR(50)
);

CREATE TABLE dim_date (
    date         DATE,
    year         INTEGER,
    quarter      VARCHAR(10),
    month        INTEGER,
    month_name   VARCHAR(20),
    week         INTEGER,
    day          INTEGER,
    weekday      VARCHAR(20),
    is_weekend   BOOLEAN
);

CREATE TABLE fact_engineering_deliverables (
    deliverable_id            VARCHAR(20),
    project_id                VARCHAR(20),
    document_id               VARCHAR(150),
    document_title            VARCHAR(250),
    discipline_id             VARCHAR(20),
    document_type_id          VARCHAR(20),
    equipment_id              VARCHAR(20),
    responsible_engineer_id   VARCHAR(20),
    status_id                 VARCHAR(20),
    revision_number           INTEGER,
    planned_submission_date   DATE,
    actual_submission_date    DATE,
    planned_approval_date     DATE,
    actual_approval_date      DATE,
    review_cycle_count        INTEGER,
    created_date              DATE,
    last_updated_date         DATE,
    comments                  TEXT
);

CREATE INDEX idx_fact_project_id
ON fact_engineering_deliverables(project_id);

CREATE INDEX idx_fact_discipline_id
ON fact_engineering_deliverables(discipline_id);

CREATE INDEX idx_fact_document_type_id
ON fact_engineering_deliverables(document_type_id);

CREATE INDEX idx_fact_status_id
ON fact_engineering_deliverables(status_id);

CREATE INDEX idx_fact_engineer_id
ON fact_engineering_deliverables(responsible_engineer_id);

CREATE INDEX idx_fact_equipment_id
ON fact_engineering_deliverables(equipment_id);

CREATE INDEX idx_fact_planned_submission_date
ON fact_engineering_deliverables(planned_submission_date);

CREATE INDEX idx_fact_document_id
ON fact_engineering_deliverables(document_id);

-- Quick validation queries after importing CSVs:
-- SELECT COUNT(*) FROM fact_engineering_deliverables;
-- SELECT COUNT(*) FROM dim_project;
-- SELECT COUNT(*) FROM dim_discipline;
-- SELECT COUNT(*) FROM dim_document_type;
-- SELECT COUNT(*) FROM dim_status;
-- SELECT COUNT(*) FROM dim_engineer;
-- SELECT COUNT(*) FROM dim_equipment;
-- SELECT COUNT(*) FROM dim_date;
