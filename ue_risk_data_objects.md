# UE Risk Scoring Tool — Data Objects Specification

This document defines the Snowflake objects required to feed the **UE Risk Scoring Tool** (`ue_risk_tool.py`). The app currently uses mock data generated in-app. The goal is to replace that with a single **view** backed by real source tables, refreshed daily.

---

## Target Output: `V_UE_RISK_DAILY_CENSUS`

The app expects **one row per intubated patient** in LC 22, LC NICU, or LC PICU on the census date. Every column below must be present.

| Column | Type | Description | Scoring Rule |
|---|---|---|---|
| `PATIENT_ID` | `NUMBER` | Unique patient encounter ID | Identity |
| `PATIENT_NAME` | `VARCHAR` | Display name (`Last, First`) | Display only |
| `MRN` | `VARCHAR` | Medical record number | Display only |
| `DEPARTMENT` | `VARCHAR` | Unit: `LC 22`, `LC NICU`, or `LC PICU` | Filter + mobility trigger lookup |
| `BED` | `VARCHAR` | Bed number/label | Display only |
| `SERVICE` | `VARCHAR` | Attending service (e.g., `Pulmonology`, `Cardiac Surgery`, `Neonatology`) | Filter only |
| `AGE_MONTHS` | `NUMBER` | Patient age in months | Display only |
| `CAPD_VALUE` | `NUMBER` | Most recent CAP-D (Cornell Assessment of Pediatric Delirium) score | +1 if >= 9 |
| `EMESIS_FLAG` | `BOOLEAN` | Emesis documented in past 24 h | +1 if TRUE |
| `SUCTION_COUNT` | `NUMBER` | Number of oral/ET suction events in past 24 h | +1 if >= 7 (only when EMESIS_FLAG is FALSE) |
| `UE_HISTORY` | `BOOLEAN` | Any unplanned extubation for this patient in the past 2 years | +1 if TRUE |
| `MOBILITY_LEVEL` | `VARCHAR` | Current mobility order/status | +1 if matches department-specific trigger level (see below) |
| `PRONE_YESTERDAY` | `BOOLEAN` | Patient was proned on the prior calendar day | +1 if either PRONE flag is TRUE |
| `PRONE_TODAY` | `BOOLEAN` | Patient is proned today | (same as above) |
| `RETAPE_COUNT` | `NUMBER` | Number of ET tube retapes in past 24 h | +1 if >= 2 |
| `TUBE_MOVED` | `BOOLEAN` | ET tube position changed (not a scheduled retape) in past 24 h | +1 if TRUE (only when RETAPE_COUNT < 2) |
| `SEDATION_DOSES_24H` | `NUMBER` | Total PRN sedation/analgesic bolus doses in past 24 h | +1 if >= 4 |
| `WEANING_ACTIVE` | `BOOLEAN` | Patient is on an active ventilator weaning protocol | +1 if TRUE |
| `DIFFICULT_AIRWAY` | `BOOLEAN` | Difficult airway flag in the chart | +1 if TRUE |
| `ETT_ROUTE` | `VARCHAR` | `Oral` or `Nasal` | Determines which standard securement set to compare against |
| `SECUREMENT_SET` | `VARCHAR` | Comma-separated list of securement devices currently in use | +1 if set does not match standard (see below) |
| `ETT_DEPTH_CM` | `NUMBER` | ET tube depth at the lip/nare in cm | +2 if <= 7; +1 if 8-9; 0 if >= 10 |
| `RACE` | `VARCHAR` | Patient race/ethnicity | +1 if not `White` |
| `LANGUAGE` | `VARCHAR` | Patient preferred language | +1 if not `English` |
| `VISITOR_PRESENT` | `BOOLEAN` | Visitor/family member present at bedside in past 24 h | +1 if FALSE (no visitor) |
| `CENSUS_DATE` | `DATE` | Date this row represents | Filter: app defaults to today, supports prior-day lookback |

---

## Reference Constants (app-side, not in Snowflake)

These are embedded in the app and do **not** need their own tables, but the source queries must produce values that align with them.

### Mobility Trigger Levels

| Department | Trigger Value (scores +1) |
|---|---|
| `LC 22` | `Ambulatory` |
| `LC NICU` | `Active / moving in bed` |
| `LC PICU` | `Ambulatory` |

`MOBILITY_LEVEL` must use these exact strings for the trigger logic to work.

### Standard Securement Sets

| ETT Route | Standard Set (no points if matched exactly) |
|---|---|
| `Oral` | `Cloth tape`, `Duoderm`, `ET tube holder` |
| `Nasal` | `Duoderm`, `Nare device`, `Tegaderm` |

`SECUREMENT_SET` should be a **comma-separated, alphabetically sorted** list of device names. If the set does not exactly match the standard for the route, the patient scores +1.

### Risk Thresholds

| Level | Score Range |
|---|---|
| High | >= 7 |
| Medium | 4 - 6 |
| Low | 0 - 3 |

---

## Source System Mapping

Below is a suggested mapping of each column to its likely Epic/EHR source. This is what the Snowflake Cortex query or ETL needs to resolve.

| Column | Likely Source | Notes |
|---|---|---|
| `PATIENT_ID` | ADT encounter ID | Current inpatient encounter |
| `PATIENT_NAME` | ADT / patient demographics | `Last, First` format |
| `MRN` | ADT / patient demographics | |
| `DEPARTMENT` | ADT census | Must resolve to `LC 22`, `LC NICU`, or `LC PICU` |
| `BED` | ADT census | Bed label/number |
| `SERVICE` | ADT attending service | |
| `AGE_MONTHS` | Patient demographics (DOB) | `DATEDIFF('month', DOB, CURRENT_DATE())` |
| `CAPD_VALUE` | Flowsheet / nursing assessment | Most recent CAP-D score in past 24 h; NULL if not assessed (treat as 0) |
| `EMESIS_FLAG` | Flowsheet / nursing documentation | Any emesis charted in past 24 h |
| `SUCTION_COUNT` | Flowsheet / respiratory therapy | Count of suction events documented in past 24 h |
| `UE_HISTORY` | Safety event system (e.g., RL Datix) or problem list | Any UE event for this MRN in past 2 years |
| `MOBILITY_LEVEL` | Activity order or mobility flowsheet | Must match department-specific string values above |
| `PRONE_YESTERDAY` | Flowsheet / positioning documentation | Prone position documented on `CURRENT_DATE() - 1` |
| `PRONE_TODAY` | Flowsheet / positioning documentation | Prone position documented on `CURRENT_DATE()` |
| `RETAPE_COUNT` | Flowsheet / respiratory therapy | Count of retape events in past 24 h |
| `TUBE_MOVED` | Flowsheet / respiratory therapy | ET tube depth change without scheduled retape |
| `SEDATION_DOSES_24H` | MAR (Medication Administration Record) | Count of PRN sedation/analgesic bolus doses in past 24 h |
| `WEANING_ACTIVE` | Respiratory care plan or vent order | Active weaning protocol flag |
| `DIFFICULT_AIRWAY` | Problem list, anesthesia note, or airway alert | Chart-level flag |
| `ETT_ROUTE` | Flowsheet / respiratory therapy | `Oral` or `Nasal` |
| `SECUREMENT_SET` | Flowsheet / respiratory therapy | Devices documented at last assessment, comma-separated, alpha-sorted |
| `ETT_DEPTH_CM` | Flowsheet / respiratory therapy | Most recent documented depth at lip/nare |
| `RACE` | Patient demographics | |
| `LANGUAGE` | Patient demographics | Preferred language |
| `VISITOR_PRESENT` | Visitor log or nursing assessment | Any visitor documented in past 24 h |
| `CENSUS_DATE` | ADT census / derived | One row per patient per day; retained historically for lookback |

---

## Snowflake Object Summary

| Object | Type | Purpose |
|---|---|---|
| `V_UE_RISK_DAILY_CENSUS` | View | **Primary object consumed by the app.** One row per intubated patient per census date. Retains historical rows for prior-day lookback. Joins all sources below. |
| `T_ADT_CENSUS` | Table / View | Historical inpatient census filtered to LC 22 / LC NICU / LC PICU with active ET tube. One row per patient per `CENSUS_DATE`. |
| `T_PATIENT_DEMOGRAPHICS` | Table / View | Name, MRN, DOB, race, preferred language |
| `T_FLOWSHEET_CAPD` | Table / View | CAP-D assessment scores by encounter + timestamp |
| `T_FLOWSHEET_EMESIS` | Table / View | Emesis documentation events |
| `T_FLOWSHEET_SUCTION` | Table / View | Suction events by encounter + timestamp |
| `T_SAFETY_EVENTS_UE` | Table / View | Unplanned extubation history from safety reporting system |
| `T_FLOWSHEET_MOBILITY` | Table / View | Mobility level/order by encounter |
| `T_FLOWSHEET_POSITIONING` | Table / View | Prone positioning documentation by encounter + date |
| `T_FLOWSHEET_RETAPE` | Table / View | ET tube retape and depth-change events |
| `T_MAR_SEDATION` | Table / View | PRN sedation/analgesic administrations from MAR |
| `T_RESPIRATORY_PLAN` | Table / View | Weaning protocol status, ETT route, depth, securement devices |
| `T_AIRWAY_ALERTS` | Table / View | Difficult airway flags from problem list or anesthesia |
| `T_VISITOR_LOG` | Table / View | Visitor presence documentation |

---

## SQL Skeleton for `V_UE_RISK_DAILY_CENSUS`

```sql
CREATE OR REPLACE VIEW V_UE_RISK_DAILY_CENSUS AS
SELECT
    c.ENCOUNTER_ID                          AS PATIENT_ID,
    d.LAST_NAME || ', ' || d.FIRST_NAME     AS PATIENT_NAME,
    d.MRN                                   AS MRN,
    c.DEPARTMENT                            AS DEPARTMENT,
    c.BED                                   AS BED,
    c.SERVICE                               AS SERVICE,
    DATEDIFF('month', d.DOB, c.CENSUS_DATE)  AS AGE_MONTHS,

    -- CAP-D (most recent in 24 h)
    COALESCE(capd.VALUE, 0)                 AS CAPD_VALUE,

    -- Emesis (any in 24 h)
    COALESCE(em.EMESIS_FLAG, FALSE)         AS EMESIS_FLAG,

    -- Suction count (24 h)
    COALESCE(suc.SUCTION_COUNT, 0)          AS SUCTION_COUNT,

    -- UE history (2 yr lookback)
    COALESCE(ue.HAS_PRIOR_UE, FALSE)        AS UE_HISTORY,

    -- Mobility
    COALESCE(mob.MOBILITY_LEVEL, 'Unknown') AS MOBILITY_LEVEL,

    -- Prone positioning
    COALESCE(pos_y.PRONE_FLAG, FALSE)       AS PRONE_YESTERDAY,
    COALESCE(pos_t.PRONE_FLAG, FALSE)       AS PRONE_TODAY,

    -- Retape / tube move
    COALESCE(rt.RETAPE_COUNT, 0)            AS RETAPE_COUNT,
    COALESCE(rt.TUBE_MOVED, FALSE)          AS TUBE_MOVED,

    -- Sedation
    COALESCE(sed.DOSE_COUNT, 0)             AS SEDATION_DOSES_24H,

    -- Weaning
    COALESCE(resp.WEANING_ACTIVE, FALSE)    AS WEANING_ACTIVE,

    -- Difficult airway
    COALESCE(aw.DIFFICULT_AIRWAY, FALSE)    AS DIFFICULT_AIRWAY,

    -- ETT details
    COALESCE(resp.ETT_ROUTE, 'Oral')        AS ETT_ROUTE,
    COALESCE(resp.SECUREMENT_SET, '')        AS SECUREMENT_SET,
    COALESCE(resp.ETT_DEPTH_CM, 10)          AS ETT_DEPTH_CM,

    -- Demographics / equity
    COALESCE(d.RACE, 'Unknown')             AS RACE,
    COALESCE(d.LANGUAGE, 'English')         AS LANGUAGE,

    -- Social
    COALESCE(vis.VISITOR_PRESENT, FALSE)    AS VISITOR_PRESENT,

    c.CENSUS_DATE                           AS CENSUS_DATE

FROM T_ADT_CENSUS c
JOIN T_PATIENT_DEMOGRAPHICS d     ON c.MRN = d.MRN
LEFT JOIN T_FLOWSHEET_CAPD capd   ON c.ENCOUNTER_ID = capd.ENCOUNTER_ID   -- most recent 24 h
LEFT JOIN T_FLOWSHEET_EMESIS em   ON c.ENCOUNTER_ID = em.ENCOUNTER_ID     -- any in 24 h
LEFT JOIN T_FLOWSHEET_SUCTION suc ON c.ENCOUNTER_ID = suc.ENCOUNTER_ID    -- count in 24 h
LEFT JOIN T_SAFETY_EVENTS_UE ue   ON d.MRN = ue.MRN                      -- 2 yr lookback
LEFT JOIN T_FLOWSHEET_MOBILITY mob ON c.ENCOUNTER_ID = mob.ENCOUNTER_ID
LEFT JOIN T_FLOWSHEET_POSITIONING pos_y ON c.ENCOUNTER_ID = pos_y.ENCOUNTER_ID
                                       AND pos_y.POSITION_DATE = c.CENSUS_DATE - 1
LEFT JOIN T_FLOWSHEET_POSITIONING pos_t ON c.ENCOUNTER_ID = pos_t.ENCOUNTER_ID
                                       AND pos_t.POSITION_DATE = c.CENSUS_DATE
LEFT JOIN T_FLOWSHEET_RETAPE rt   ON c.ENCOUNTER_ID = rt.ENCOUNTER_ID     -- 24 h aggregates
LEFT JOIN T_MAR_SEDATION sed      ON c.ENCOUNTER_ID = sed.ENCOUNTER_ID    -- 24 h count
LEFT JOIN T_RESPIRATORY_PLAN resp ON c.ENCOUNTER_ID = resp.ENCOUNTER_ID   -- latest assessment
LEFT JOIN T_AIRWAY_ALERTS aw      ON c.ENCOUNTER_ID = aw.ENCOUNTER_ID
LEFT JOIN T_VISITOR_LOG vis        ON c.ENCOUNTER_ID = vis.ENCOUNTER_ID   -- 24 h any

WHERE c.DEPARTMENT IN ('LC 22', 'LC NICU', 'LC PICU')
  AND c.HAS_ETT = TRUE;
-- No date filter here — view retains all historical rows.
-- The app filters by CENSUS_DATE (defaults to today, supports prior-day lookback).
```

> **Retention:** The view should retain at least **90 days** of historical census rows to support post-event review, trend analysis, and weekend catch-up workflows. The app filters to a single date at query time.

> **Note:** Each `LEFT JOIN` source likely needs its own sub-query or CTE to aggregate to one row per encounter (e.g., `MAX(CAPD_VALUE)`, `COUNT(*)` for suction, `BOOL_OR()` for flags). The skeleton above shows the join shape — the actual CTEs will depend on the source table schemas.

---

## Pain / Agitation (Future)

The scoring category **Pain / Agitation** is currently a placeholder (`TBD`, always scores 0). When ready, add these columns to the view:

| Column | Type | Description | Proposed Rule |
|---|---|---|---|
| `PAIN_SCORE` | `NUMBER` | Most recent pain assessment score (e.g., FLACC, FACES) | TBD |
| `AGITATION_SCORE` | `NUMBER` | Most recent agitation score (e.g., SBS, RASS) | TBD |

These will likely come from `T_FLOWSHEET_CAPD` or a separate pain/sedation assessment flowsheet.

---

## Snowflake Cortex Prompt

The developer already has a working query that pulls the intubated-patient census. Copy the prompt below into Snowflake Cortex and paste your existing query when indicated. Cortex will adapt the query to produce the exact output schema the app requires.

> **How to use:** Open Snowflake Cortex (or Copilot), paste the full block below, and replace `<<PASTE YOUR EXISTING QUERY HERE>>` with your current SQL.

~~~
I have an existing Snowflake query that pulls a daily census of intubated pediatric patients
in LC 22, LC NICU, and LC PICU. I need to adapt it into a view called V_UE_RISK_DAILY_CENSUS
that feeds a Streamlit risk-scoring app.

Here is my existing query:

<<PASTE YOUR EXISTING QUERY HERE>>

Please modify it to produce EXACTLY the following output schema — one row per intubated patient
per CENSUS_DATE, with all columns present and correctly typed. The app will break if columns
are missing or renamed.

Required output columns (all must be present):

| Column               | Type    | How to derive                                                              |
|----------------------|---------|----------------------------------------------------------------------------|
| PATIENT_ID           | NUMBER  | Encounter ID                                                               |
| PATIENT_NAME         | VARCHAR | "Last, First" format                                                       |
| MRN                  | VARCHAR | Medical record number                                                      |
| DEPARTMENT           | VARCHAR | Must be exactly 'LC 22', 'LC NICU', or 'LC PICU'                          |
| BED                  | VARCHAR | Bed number or label                                                        |
| SERVICE              | VARCHAR | Attending service name                                                     |
| AGE_MONTHS           | NUMBER  | DATEDIFF('month', DOB, CENSUS_DATE)                                        |
| CAPD_VALUE           | NUMBER  | Most recent CAP-D score in the 24 h before CENSUS_DATE. COALESCE to 0.    |
| EMESIS_FLAG          | BOOLEAN | TRUE if any emesis documented in 24 h before CENSUS_DATE.                  |
| SUCTION_COUNT        | NUMBER  | Count of oral/ET suction events in 24 h before CENSUS_DATE. COALESCE to 0.|
| UE_HISTORY           | BOOLEAN | TRUE if this MRN has any unplanned extubation in the prior 2 years.        |
| MOBILITY_LEVEL       | VARCHAR | Current mobility order. Must use these exact strings:                      |
|                      |         |   LC 22 / LC PICU: 'Bedrest', 'Dangle', 'Chair', 'Ambulatory'             |
|                      |         |   LC NICU: 'Minimal movement', 'Moderate movement', 'Active / moving in bed' |
| PRONE_YESTERDAY      | BOOLEAN | TRUE if patient was proned on CENSUS_DATE - 1.                             |
| PRONE_TODAY          | BOOLEAN | TRUE if patient was proned on CENSUS_DATE.                                 |
| RETAPE_COUNT         | NUMBER  | Count of ET tube retapes in 24 h before CENSUS_DATE. COALESCE to 0.       |
| TUBE_MOVED           | BOOLEAN | TRUE if ET tube depth changed (non-retape) in 24 h before CENSUS_DATE.    |
| SEDATION_DOSES_24H   | NUMBER  | Count of PRN sedation/analgesic bolus doses in 24 h. COALESCE to 0.       |
| WEANING_ACTIVE       | BOOLEAN | TRUE if patient is on an active vent weaning protocol.                     |
| DIFFICULT_AIRWAY     | BOOLEAN | TRUE if difficult airway flag exists in the chart.                         |
| ETT_ROUTE            | VARCHAR | 'Oral' or 'Nasal'.                                                        |
| SECUREMENT_SET       | VARCHAR | Comma-separated, alphabetically sorted list of securement devices.         |
|                      |         | e.g. 'Cloth tape, Duoderm, ET tube holder'                                 |
| ETT_DEPTH_CM         | NUMBER  | Most recent ET tube depth at lip/nare in cm. COALESCE to 10.              |
| RACE                 | VARCHAR | Patient race/ethnicity. COALESCE to 'Unknown'.                             |
| LANGUAGE             | VARCHAR | Patient preferred language. COALESCE to 'English'.                         |
| VISITOR_PRESENT      | BOOLEAN | TRUE if any visitor documented in 24 h before CENSUS_DATE.                 |
| CENSUS_DATE          | DATE    | The calendar date this row represents.                                     |

Important rules:
1. Do NOT filter to CURRENT_DATE(). Keep all historical dates — the app filters by date at runtime.
2. Filter to departments IN ('LC 22', 'LC NICU', 'LC PICU') and patients with an active ET tube.
3. Every BOOLEAN column must be TRUE/FALSE (not NULL). Use COALESCE(..., FALSE).
4. Every NUMBER column must not be NULL. Use COALESCE(..., 0) or COALESCE(..., 10) for ETT_DEPTH_CM.
5. SECUREMENT_SET must be alphabetically sorted and comma-separated with a space after each comma.
6. Aggregate sub-queries into CTEs so the final SELECT produces exactly one row per patient per day.
7. Retain at least 90 days of historical rows for prior-day lookback.
8. Wrap the final result as: CREATE OR REPLACE VIEW V_UE_RISK_DAILY_CENSUS AS ...

Please return the full CREATE VIEW statement with all CTEs. Add comments explaining each CTE.
~~~
