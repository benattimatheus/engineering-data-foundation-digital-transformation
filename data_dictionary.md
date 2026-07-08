# Data Dictionary

## Project

**Engineering Data Foundation & Digital Transformation Dashboard**

This data dictionary describes the main analytical datasets used in the Power BI dashboard.

The project uses synthetic data generated for portfolio purposes. No real company, employee, project, or engineering information is included.

---

## Main Analytical Views

| View | Description | Granularity |
|---|---|---|
| `vw_deliverables_overview` | Main reporting view for engineering deliverables, enriched with project, document, discipline, equipment, engineer, status, date and KPI fields. | One row per deliverable |
| `vw_data_quality_issue_rows` | Data quality and workflow issue table. Each row represents one detected issue for one deliverable. | One row per deliverable per issue |
| `vw_improvement_opportunities` | Aggregated improvement opportunity view based on issue type, severity, impact and recommended action. | One row per issue type |
| `vw_engineering_workflow_status` | Aggregated workflow status view by project, discipline and status. | One row per status/project/discipline combination |

---

# 1. `vw_deliverables_overview`

## Description

Main deliverable-level view used for the Engineering Project Overview and Workflow & Bottlenecks dashboard pages.

This view consolidates engineering deliverable information with project, document, discipline, equipment, engineer, workflow status, dates, delay indicators and data quality flags.

## Granularity

One row per engineering deliverable.

## Columns

| Column | Type | Description | Business Meaning |
|---|---|---|---|
| `deliverable_id` | Text | Unique identifier of the engineering deliverable. | Primary deliverable-level key used for counting and relationships. |
| `project_id` | Text | Unique identifier of the project. | Used to group deliverables by project. |
| `project_name` | Text | Project name. | User-friendly project label for reporting. |
| `client` | Text | Client associated with the project. | Allows client-level analysis if needed. |
| `project_phase` | Text | Current phase of the project. | Indicates whether the project is in design, execution, validation, etc. |
| `project_manager` | Text | Project manager responsible for the project. | Supports ownership and accountability analysis. |
| `project_start_date` | Date | Project start date. | Used to validate planned and actual dates. |
| `project_end_date` | Date | Project end date. | Used to validate planned and actual dates. |
| `project_status` | Text | Overall project status. | Indicates whether the project is active, delayed or on hold. |
| `document_id` | Text | Engineering document identifier. | Used for document traceability and duplicate checks. |
| `document_title` | Text | Document title. | Descriptive label of the engineering deliverable. |
| `document_type_id` | Text | Document type identifier. | Technical key for document type. |
| `document_type_name` | Text | Document type name. | Used to analyze deliverables by document type. |
| `discipline_id` | Text | Engineering discipline identifier. | Technical key for discipline. |
| `discipline_name` | Text | Engineering discipline name. | Used to analyze deliverables by discipline. |
| `equipment_id` | Text | Equipment identifier. | Technical key for equipment-related deliverables. |
| `equipment_tag` | Text | Equipment tag. | Engineering equipment reference. |
| `equipment_type` | Text | Type of equipment. | Supports equipment-level analysis. |
| `area` | Text | Plant, project or operational area. | Used to understand where the deliverable applies. |
| `system` | Text | System associated with the deliverable. | Supports system-level segmentation. |
| `criticality` | Text | Equipment or deliverable criticality. | Used to identify business or technical impact. |
| `responsible_engineer_id` | Text | Responsible engineer identifier. | Technical key for owner analysis. |
| `engineer_name` | Text | Responsible engineer name. | User-friendly owner label. |
| `engineer_role` | Text | Engineer role. | Allows analysis by role type. |
| `engineer_team` | Text | Engineer team. | Supports team-level monitoring. |
| `engineer_location` | Text | Engineer location. | Supports location-level segmentation. |
| `status_id` | Text | Workflow status identifier. | Technical key for deliverable status. |
| `status_name` | Text | Workflow status name. | Main field for deliverable status reporting. |
| `status_group` | Text | Grouped workflow status. | Simplifies workflow analysis. |
| `revision_number` | Integer | Current document revision number. | Indicates document iteration level. |
| `review_cycle_count` | Integer | Number of review cycles. | Indicates how many times the document moved through review. |
| `planned_submission_date` | Date | Planned date for document submission. | Main date used in dashboard date filtering. |
| `actual_submission_date` | Date | Actual date when the document was submitted. | Used to calculate submission variance. |
| `planned_approval_date` | Date | Planned date for approval. | Used to detect overdue approval items. |
| `actual_approval_date` | Date | Actual date when the document was approved. | Used to calculate review cycle days. |
| `created_date` | Date | Date when the deliverable record was created. | Helps understand record lifecycle. |
| `last_updated_date` | Date | Date when the deliverable record was last updated. | Helps understand record freshness. |
| `comments` | Text | Optional comments. | Contextual notes about the deliverable. |
| `reference_date` | Date | Date used as reporting reference. | Used to calculate overdue and aging indicators. |
| `is_completed` | Boolean | Indicates whether the deliverable is completed. | True when the deliverable is approved. |
| `is_closed` | Boolean | Indicates whether the deliverable is closed. | True when the deliverable is approved or cancelled. |
| `is_pending` | Boolean | Indicates whether the deliverable is still open in the workflow. | Used to calculate pending deliverables. |
| `is_overdue` | Boolean | Indicates whether the deliverable is currently overdue. | Used to calculate overdue deliverables and overdue rate. |
| `submission_variance_days` | Integer | Difference between actual and planned submission date. | Negative means early submission; positive means late submission. |
| `late_submission_days` | Integer | Number of days submitted late. | Only counts positive submission delay. |
| `current_overdue_days` | Integer | Current number of overdue days for open items. | Measures active delay exposure. |
| `review_cycle_days` | Integer | Days between actual submission and actual approval. | Used to measure approval cycle performance. |
| `days_under_review` | Integer | Days since submission for items currently under review. | Used to identify aging review backlog. |
| `data_quality_issue_count` | Integer | Total number of issues detected for the deliverable. | Indicates issue volume at deliverable level. |
| `distinct_data_quality_issue_count` | Integer | Number of distinct issue types detected for the deliverable. | Indicates diversity of issues for the deliverable. |
| `has_data_quality_issue` | Boolean | Indicates whether the deliverable has at least one issue. | Used to identify affected deliverables. |

## Main Power BI Measures Based on This View

| Measure | Description |
|---|---|
| `Total Deliverables` | Distinct count of deliverables. |
| `Completed Deliverables` | Deliverables with `is_completed = TRUE`. |
| `Pending Deliverables` | Deliverables with `is_pending = TRUE`. |
| `Overdue Deliverables` | Deliverables with `is_overdue = TRUE`. |
| `Completion Rate` | Completed deliverables divided by total deliverables. |
| `Overdue Rate` | Overdue deliverables divided by total deliverables. |
| `Documents Under Review` | Deliverables where `status_name = "Under Review"`. |
| `Rejected Deliverables` | Deliverables where `status_name = "Rejected"`. |
| `Average Review Cycle Days` | Average of `review_cycle_days`. |
| `Average Days Under Review` | Average of `days_under_review`. |

---

# 2. `vw_data_quality_issue_rows`

## Description

Issue-level view used for the Data Quality Dashboard and part of the Workflow & Bottlenecks page.

Each row represents one detected issue associated with one engineering deliverable.

## Granularity

One row per deliverable per issue.

A single deliverable may appear more than once if it has multiple issues.

## Columns

| Column | Type | Description | Business Meaning |
|---|---|---|---|
| `deliverable_id` | Text | Unique identifier of the deliverable. | Links the issue back to the deliverable. |
| `document_id` | Text | Engineering document identifier. | Used to trace the affected document. |
| `project_id` | Text | Project identifier. | Used to group issues by project. |
| `project_name` | Text | Project name. | User-friendly project label. |
| `discipline_id` | Text | Discipline identifier. | Technical key for discipline. |
| `discipline_name` | Text | Discipline name. | Used to group issues by engineering discipline. |
| `document_type_id` | Text | Document type identifier. | Technical key for document type. |
| `document_type_name` | Text | Document type name. | Used to group issues by document type. |
| `equipment_id` | Text | Equipment identifier. | Links issues to equipment records when applicable. |
| `equipment_tag` | Text | Equipment tag. | User-friendly equipment reference. |
| `responsible_engineer_id` | Text | Responsible engineer identifier. | Used to analyze issues by owner. |
| `engineer_name` | Text | Responsible engineer name. | User-friendly engineer label. |
| `status_id` | Text | Workflow status identifier. | Technical key for status. |
| `status_name` | Text | Workflow status name. | Indicates the deliverable status when the issue was detected. |
| `issue_category` | Text | Broad issue category. | Groups issues into business-relevant categories. |
| `issue_type` | Text | Specific issue type. | Main issue-level classification used in charts. |
| `severity` | Text | Original severity classification. | Indicates issue impact before Power BI adjustments. |
| `issue_description` | Text | Explanation of the detected issue. | Provides operational meaning for each issue. |

## Issue Categories

| Category | Description |
|---|---|
| `Delay` | Issues related to overdue submissions or approvals. |
| `Missing Metadata` | Issues caused by incomplete required fields. |
| `Workflow Issue` | Issues related to review cycle, approval status or workflow consistency. |
| `Duplicate` | Issues caused by repeated document identifiers. |
| `Invalid Value` | Issues caused by invalid or unexpected field values. |
| `Reference Integrity` | Issues related to invalid or inconsistent reference records. |

## Main Issue Types

| Issue Type | Description |
|---|---|
| `Overdue Submission` | Planned submission date has passed and the deliverable has not been submitted. |
| `Overdue Approval` | Planned approval date has passed and the deliverable has not been approved. |
| `Missing Project Phase` | Project phase is missing. |
| `Long Review Cycle` | Document has remained under review longer than the defined threshold. |
| `Duplicate Document ID` | Document identifier appears more than once. |
| `Missing Equipment` | Equipment reference is missing. |
| `Missing Owner` | Responsible engineer is missing. |
| `Invalid Equipment Criticality` | Criticality value is invalid or outside the expected domain. |
| `Invalid Revision Number` | Revision number is invalid. |
| `Missing Discipline` | Engineering discipline is missing. |
| `Missing Document Type` | Document type is missing. |
| `Approved Deliverable Missing Actual Approval Date` | Deliverable is approved but the actual approval date is missing. |
| `Invalid Status` | Workflow status is invalid. |

## Main Power BI Measures Based on This View

| Measure | Description |
|---|---|
| `Total Data Quality Issues` | Number of rows in `vw_data_quality_issue_rows`. |
| `Deliverables With Issues` | Distinct count of deliverables with at least one issue. |
| `Data Quality Issue Rate` | Deliverables with issues divided by total deliverables. |
| `High Severity Issues` | Count of issues classified as high severity. |
| `Missing Metadata Issues` | Count of issues where `issue_category = "Missing Metadata"`. |
| `Duplicate Document IDs` | Count of issues where `issue_type = "Duplicate Document ID"`. |
| `Workflow Bottleneck Issues` | Count of issues where category is `Delay` or `Workflow Issue`. |
| `Overdue Submission Issues` | Count of `Overdue Submission` issues. |
| `Overdue Approval Issues` | Count of `Overdue Approval` issues. |
| `Long Review Cycle Items` | Count of `Long Review Cycle` issues. |

---

# 3. `vw_improvement_opportunities`

## Description

Aggregated view used for the Improvement Opportunities page.

This view summarizes issue types and translates them into prioritized improvement opportunities based on issue volume, affected areas, severity and recommended actions.

## Granularity

One row per issue type.

## Columns

| Column | Type | Description | Business Meaning |
|---|---|---|---|
| `issue_category` | Text | Broad issue category. | Groups opportunities by type of problem. |
| `issue_type` | Text | Specific issue type. | Defines the improvement opportunity. |
| `severity` | Text | Severity level associated with the issue type. | Used to evaluate business impact. |
| `issue_count` | Integer | Number of detected issues of this type. | Measures issue volume. |
| `affected_deliverables` | Integer | Number of affected deliverable records for this issue type. | Measures operational impact. |
| `affected_projects` | Integer | Number of projects affected by this issue type. | Measures project spread. |
| `affected_disciplines` | Integer | Number of disciplines affected by this issue type. | Measures discipline spread. |
| `severity_weight` | Integer | Numeric weight assigned to severity. | Used to calculate priority score. |
| `priority_score` | Integer | Raw priority score based on impact and severity. | Used to rank improvement opportunities. |
| `recommended_action` | Text | Suggested action to reduce or fix the issue. | Used in the action plan table. |

## Additional Power BI Calculated Columns

| Column | Type | Description |
|---|---|---|
| `Priority Score 0-100` | Decimal | Normalized version of `priority_score`, scaled from 0 to 100. |
| `Priority Tier` | Text | Classifies opportunities as High, Medium or Low Priority. |
| `Action Type` | Text | Groups recommended actions into strategic action groups. |
| `Recommended Action Clean` | Text | Cleaned and more specific version of the recommended action text. |

## Priority Tier Logic

| Tier | Rule | Meaning |
|---|---|---|
| `High Priority` | Priority Score 0-100 >= 70 | Highest impact opportunities to address first. |
| `Medium Priority` | Priority Score 0-100 >= 25 and < 70 | Relevant opportunities with moderate impact. |
| `Low Priority` | Priority Score 0-100 < 25 | Lower-priority or more localized actions. |

## Action Type Logic

| Action Type | Description | Example Issues |
|---|---|---|
| `Workflow acceleration` | Actions focused on reducing delays and improving approval flow. | Overdue Submission, Overdue Approval, Long Review Cycle |
| `Metadata governance` | Actions focused on improving required metadata completeness. | Missing Owner, Missing Equipment, Missing Project Phase |
| `Document control` | Actions focused on improving document traceability. | Duplicate Document ID |
| `Validation rules` | Actions focused on preventing invalid field values. | Invalid Revision Number, Invalid Equipment Criticality |
| `Process review` | Actions requiring process or rule review. | Approved Deliverable Missing Actual Approval Date |

## Main Power BI Measures Based on This View

| Measure | Description |
|---|---|
| `Total Opportunities` | Number of improvement opportunities. |
| `High Priority Opportunities` | Number of opportunities classified as High Priority. |
| `Total Related Issues` | Sum of issue counts linked to opportunities. |
| `Average Priority Score` | Average normalized priority score. |
| `Action Types` | Distinct count of action types. |

---

# 4. `vw_engineering_workflow_status`

## Description

Aggregated workflow view used to support workflow and bottleneck analysis.

This view summarizes deliverable counts, overdue counts, quality issue counts and aging metrics by project, discipline and workflow status.

## Granularity

One row per status, project and discipline combination.

## Columns

| Column | Type | Description | Business Meaning |
|---|---|---|---|
| `status_id` | Text | Workflow status identifier. | Technical key for status. |
| `status_name` | Text | Workflow status name. | Main workflow status label. |
| `status_group` | Text | Grouped workflow status. | Simplifies workflow reporting. |
| `project_id` | Text | Project identifier. | Used to aggregate workflow status by project. |
| `project_name` | Text | Project name. | User-friendly project label. |
| `discipline_id` | Text | Discipline identifier. | Technical key for engineering discipline. |
| `discipline_name` | Text | Discipline name. | Used to aggregate workflow status by discipline. |
| `total_deliverables` | Integer | Number of deliverables in the group. | Measures workflow volume. |
| `overdue_deliverables` | Integer | Number of overdue deliverables in the group. | Measures active delay exposure. |
| `deliverables_with_quality_issues` | Integer | Number of deliverables with detected issues. | Measures quality exposure in the group. |
| `average_current_overdue_days` | Decimal | Average current overdue days for the group. | Indicates delay severity. |
| `average_days_under_review` | Decimal | Average days under review for the group. | Indicates review backlog intensity. |

---

# 5. Date Dimension

## Description

The date dimension is used to support time-based analysis in Power BI.

The active relationship should connect:

```text
dim_date[date] → vw_deliverables_overview[planned_submission_date]
```

## Recommended Columns

| Column | Type | Description | Business Meaning |
|---|---|---|---|
| `date` | Date | Calendar date. | Main date field used in relationships. |
| `year` | Integer | Calendar year. | Used for yearly analysis. |
| `month_number` | Integer | Month number from 1 to 12. | Used for sorting months. |
| `month_name` | Text | Month name. | Used for readable labels. |
| `month_year` | Text | Month-year label such as Jan-25. | Used in time-series charts. |
| `month_year_sort` | Integer | Numeric sorting key in YYYYMM format. | Used to sort `month_year` correctly. |
| `quarter` | Text | Calendar quarter. | Used for quarterly analysis. |

---

# 6. Power BI Calculated Columns

## `Review Aging Bucket`

Used in the Workflow & Bottlenecks page to group documents currently under review by aging range.

```DAX
Review Aging Bucket =
SWITCH(
    TRUE(),
    vw_deliverables_overview[status_name] <> "Under Review", "6. Not under review",
    ISBLANK(vw_deliverables_overview[days_under_review]), "6. Not under review",
    vw_deliverables_overview[days_under_review] <= 30, "1. 0-30 days",
    vw_deliverables_overview[days_under_review] <= 60, "2. 31-60 days",
    vw_deliverables_overview[days_under_review] <= 90, "3. 61-90 days",
    vw_deliverables_overview[days_under_review] <= 180, "4. 91-180 days",
    "5. 180+ days"
)
```

## `Severity Adjusted`

Used in the Data Quality Dashboard to create a more balanced severity distribution.

```DAX
Severity Adjusted =
SWITCH(
    TRUE(),

    vw_data_quality_issue_rows[issue_type] IN {
        "Approved Deliverable Missing Actual Approval Date",
        "Invalid Status",
        "Duplicate Document ID",
        "Overdue Approval"
    }, "High",

    vw_data_quality_issue_rows[issue_type] IN {
        "Missing Project Phase",
        "Invalid Equipment Criticality",
        "Invalid Revision Number",
        "Suspicious Early Submission"
    }, "Low",

    "Medium"
)
```

## `Priority Score 0-100`

Used in the Improvement Opportunities page to normalize the raw priority score.

```DAX
Priority Score 0-100 =
VAR MaxScore =
    MAXX(
        ALL(vw_improvement_opportunities),
        vw_improvement_opportunities[priority_score]
    )
RETURN
DIVIDE(
    vw_improvement_opportunities[priority_score],
    MaxScore
) * 100
```

## `Priority Tier`

Used to classify improvement opportunities into High, Medium or Low Priority.

```DAX
Priority Tier =
SWITCH(
    TRUE(),
    vw_improvement_opportunities[Priority Score 0-100] >= 70, "High Priority",
    vw_improvement_opportunities[Priority Score 0-100] >= 25, "Medium Priority",
    "Low Priority"
)
```

## `Action Type`

Used to group recommended actions into strategic improvement areas.

```DAX
Action Type =
SWITCH(
    TRUE(),

    vw_improvement_opportunities[issue_type] IN {
        "Overdue Submission",
        "Overdue Approval",
        "Long Review Cycle",
        "Approved Deliverable Missing Actual Approval Date"
    }, "Workflow acceleration",

    vw_improvement_opportunities[issue_type] IN {
        "Missing Owner",
        "Missing Equipment",
        "Missing Discipline",
        "Missing Document Type",
        "Missing Project Phase"
    }, "Metadata governance",

    vw_improvement_opportunities[issue_type] = "Duplicate Document ID",
    "Document control",

    vw_improvement_opportunities[issue_type] IN {
        "Invalid Equipment Criticality",
        "Invalid Revision Number"
    }, "Validation rules",

    vw_improvement_opportunities[issue_type] = "Invalid Status",
    "Reference data control",

    "Process review"
)
```

---

# 7. Relationship Recommendations

| From Table | From Column | To Table | To Column | Relationship |
|---|---|---|---|---|
| `dim_date` | `date` | `vw_deliverables_overview` | `planned_submission_date` | One-to-many |
| `vw_deliverables_overview` | `deliverable_id` | `vw_data_quality_issue_rows` | `deliverable_id` | One-to-many |
| `vw_improvement_opportunities` | N/A | N/A | N/A | Can remain disconnected |

---

# 8. Important Business Rules

| Rule | Description |
|---|---|
| Completed deliverable | A deliverable is completed when `status_name = "Approved"`. |
| Pending deliverable | A deliverable is pending when it is still open in the workflow. |
| Closed deliverable | A deliverable is closed when it is approved or cancelled. |
| Overdue deliverable | A deliverable is overdue when it is open and has passed the relevant planned date. |
| Data quality issue rate | Distinct deliverables with issues divided by total deliverables. |
| Priority score | Raw score based on issue count and severity weight. |
| Normalized priority score | Priority score scaled from 0 to 100 for dashboard readability. |
| Review aging | Days since submission for documents currently under review. |

---

# 9. Notes

- The dataset is synthetic and designed for portfolio demonstration.
- A deliverable may be completed and still have data quality issues.
- A deliverable may have more than one issue.
- `Deliverables With Issues` is a distinct count of deliverables, while `Total Data Quality Issues` counts issue rows.
- `affected_deliverables` in the improvement opportunities view is aggregated by issue type and should not be interpreted as a global distinct count across all opportunities.
- `priority_score` is useful for ranking, but `Priority Score 0-100` is better for dashboard visualization.
- The Power BI dashboard uses `planned_submission_date` as the primary date relationship.
