"""
UE Risk Scoring Tool — Streamlit Application
=============================================
Pediatric unplanned-extubation risk scoring for LC 22, LC NICU, and LC PICU.
Daily census tool used by the clinical team to prioritize prevention efforts.

Run:  streamlit run ue_risk_tool.py
"""

import streamlit as st
import pandas as pd
import datetime
import random
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="UE Risk Scoring Tool",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — matching NAKI / Safety Dashboard skin
# ──────────────────────────────────────────────────────────────────────────────
st.html("""
<style>
    /* ── Global ────────────────────────────────────────────────── */
    .block-container { padding-top: 1.5rem; }

    /* ── Professional Sidebar ─────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: none;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdown"] { color: #cbd5e1; }
    [data-testid="stSidebar"] .stRadio > label { display: none !important; }
    [data-testid="stSidebar"] .stRadio > div { gap: 1px !important; }
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent;
        border-radius: 6px;
        padding: 0 !important;
        margin: 0 !important;
        min-height: unset !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
    [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) {
        background: rgba(255,255,255,0.10) !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label p {
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
        padding: 6px 8px !important;
        line-height: 1.2 !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label:has(input:checked) p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #94a3b8 !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stDateInput {
        margin-bottom: 0 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.08) !important;
        margin: 0.3rem 0 !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.08) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.3rem 0.75rem !important;
        transition: all 0.15s ease !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.14) !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] [data-testid="stHtml"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Logo area */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        background: #ffffff;
        border-radius: 8px;
        padding: 6px 10px;
        display: inline-block;
        margin-bottom: 0 !important;
    }
    .sidebar-logo {
        padding: 0 0 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .sidebar-logo-title { font-size: 0.92rem; font-weight: 700; color: #ffffff; line-height: 1.2; }
    .sidebar-logo-sub { font-size: 0.68rem; font-weight: 500; color: #64748b; margin-top: 1px; }

    /* Section labels */
    .nav-section-label {
        font-size: 0.65rem; font-weight: 700; color: #475569;
        text-transform: uppercase; letter-spacing: 0.08em;
        padding: 0.25rem 0 0.15rem 0.25rem;
        margin: 0;
    }

    /* Version badge */
    .sidebar-version {
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 6px; padding: 3px 8px;
        font-size: 0.65rem; color: #64748b; font-weight: 500;
        margin: 0;
    }
    .sidebar-version .dot {
        width: 5px; height: 5px; border-radius: 50%;
        background: #43A047; display: inline-block;
    }

    /* ── Card containers ──────────────────────────────────────── */
    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1E88E5;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .card-red { border-left-color: #E53935; }
    .card-orange { border-left-color: #FB8C00; }
    .card-green { border-left-color: #43A047; }
    .card-purple { border-left-color: #8b5cf6; }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* ── KPI Metric Cards ─────────────────────────────────────── */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 0.75rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.15s;
        min-height: 90px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1;
    }
    .kpi-value.urgent { color: #E53935; }
    .kpi-value.warn { color: #FB8C00; }
    .kpi-value.ok { color: #43A047; }
    .kpi-value.primary { color: #1E88E5; }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    .kpi-border-blue { border-top: 3px solid #1E88E5; }
    .kpi-border-orange { border-top: 3px solid #FB8C00; }
    .kpi-border-red { border-top: 3px solid #E53935; }
    .kpi-border-green { border-top: 3px solid #43A047; }
    .kpi-border-purple { border-top: 3px solid #8b5cf6; }
    [data-testid="stHtml"]:has(.kpi-card) {
        height: 100%;
    }

    /* ── Badges / Pills ───────────────────────────────────────── */
    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        line-height: 1.5;
    }
    .badge-green  { background: #dcfce7; color: #166534; }
    .badge-red    { background: #fee2e2; color: #991b1b; }
    .badge-orange { background: #ffedd5; color: #9a3412; }
    .badge-blue   { background: #dbeafe; color: #1e40af; }
    .badge-gray   { background: #f1f5f9; color: #475569; }
    .badge-yellow { background: #fef9c3; color: #854d0e; }

    /* ── Drug / tag chips ──────────────────────────────────────── */
    .chip {
        display: inline-block;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 2px 10px;
        font-size: 0.78rem;
        font-weight: 500;
        margin-right: 4px;
        margin-bottom: 2px;
    }

    /* ── Severity badges ──────────────────────────────────────── */
    .sev-high {
        display: inline-block; padding: 3px 14px; border-radius: 6px;
        font-size: 0.78rem; font-weight: 700;
        background: #E53935; color: #fff;
    }
    .sev-med {
        display: inline-block; padding: 3px 14px; border-radius: 6px;
        font-size: 0.78rem; font-weight: 700;
        background: #FB8C00; color: #fff;
    }
    .sev-low {
        display: inline-block; padding: 3px 14px; border-radius: 6px;
        font-size: 0.78rem; font-weight: 700;
        background: #43A047; color: #fff;
    }

    /* ── Tables ────────────────────────────────────────────────── */
    .data-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.88rem;
    }
    .data-table th {
        text-align: left;
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748b;
        padding: 10px 12px;
        border-bottom: 2px solid #e2e8f0;
    }
    .data-table td {
        padding: 10px 12px;
        color: #334155;
        border-bottom: 1px solid #f1f5f9;
        vertical-align: middle;
    }
    .data-table tr:hover td { background: #f8fafc; }

    /* ── Heatmap cells ─────────────────────────────────────────── */
    .heat-high { background: #fee2e2; color: #991b1b; font-weight: 700; padding: 8px 16px; border-radius: 6px; }
    .heat-med  { background: #ffedd5; color: #9a3412; font-weight: 700; padding: 8px 16px; border-radius: 6px; }
    .heat-low  { background: #dcfce7; color: #166534; font-weight: 700; padding: 8px 16px; border-radius: 6px; }

    /* ── Summary grid ──────────────────────────────────────────── */
    .summary-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .summary-value {
        font-size: 0.92rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.4rem;
    }

    /* ── Progress bars (custom) ────────────────────────────────── */
    .bar-container {
        background: #f1f5f9;
        border-radius: 6px;
        height: 22px;
        width: 100%;
        overflow: hidden;
        margin-bottom: 6px;
    }
    .bar-fill {
        height: 100%;
        border-radius: 6px;
        display: flex;
        align-items: center;
        padding-left: 8px;
        font-size: 0.72rem;
        font-weight: 700;
        color: #fff;
    }
    .bar-blue { background: #1E88E5; }
    .bar-red { background: #E53935; }
    .bar-orange { background: #FB8C00; }
    .bar-green { background: #43A047; }
    .bar-purple { background: #8b5cf6; }
    .bar-teal { background: #0d9488; }

    /* ── Filter bar ────────────────────────────────────────────── */
    .filter-bar {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 1.25rem;
    }

    /* ── Narrative / quote blocks ──────────────────────────────── */
    .narrative {
        background: #f8fafc;
        border-left: 3px solid #1E88E5;
        padding: 0.6rem 1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #475569;
        margin-top: 0.25rem;
    }

    /* hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── UE Risk Tool — score cells ───────────────────────────── */
    .score-cell-high {
        display: inline-block; padding: 4px 14px; border-radius: 8px;
        font-weight: 800; font-size: 1rem;
        background: #fee2e2; color: #991b1b;
    }
    .score-cell-med {
        display: inline-block; padding: 4px 14px; border-radius: 8px;
        font-weight: 800; font-size: 1rem;
        background: #ffedd5; color: #9a3412;
    }
    .score-cell-low {
        display: inline-block; padding: 4px 14px; border-radius: 8px;
        font-weight: 800; font-size: 1rem;
        background: #dcfce7; color: #166534;
    }

    /* ── Detail section labels ────────────────────────────────── */
    .detail-section-label {
        font-size: 0.72rem; font-weight: 700; color: #475569;
        text-transform: uppercase; letter-spacing: 0.06em;
        padding: 0.5rem 0 0.2rem 0;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 0.3rem;
    }

    /* ── Score breakdown rows ─────────────────────────────────── */
    .score-item-row {
        display: flex; align-items: center; gap: 8px;
        padding: 6px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .score-item-label {
        flex: 1;
        font-size: 0.85rem; font-weight: 600; color: #334155;
    }
    .score-item-value {
        flex: 2;
        font-size: 0.82rem; color: #64748b;
    }
    .score-item-pts {
        min-width: 42px; text-align: center;
        padding: 2px 10px; border-radius: 6px;
        font-size: 0.78rem; font-weight: 700;
    }
    .pts-on  { background: #fee2e2; color: #991b1b; }
    .pts-off { background: #f1f5f9; color: #94a3b8; }
    .pts-2   { background: #fecaca; color: #7f1d1d; }

    /* Triggered rows get subtle highlight */
    .data-table tr.row-triggered td { background: #fef2f2; }
    .data-table tr.row-triggered:hover td { background: #fee2e2; }
    /* Total row at bottom of breakdown */
    .data-table tr.row-total td {
        border-top: 2px solid #e2e8f0;
        font-weight: 700; color: #1e293b;
        background: #f8fafc;
    }

    /* ── Chip colors for key factors — varied by category ────── */
    .chip-factor {
        display: inline-block; border-radius: 6px;
        padding: 2px 10px; font-size: 0.72rem; font-weight: 600;
        margin-right: 4px; margin-bottom: 2px;
    }
    .chip-factor-red    { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    .chip-factor-orange { background: #ffedd5; color: #9a3412; border: 1px solid #fed7aa; }
    .chip-factor-blue   { background: #dbeafe; color: #1e40af; border: 1px solid #bfdbfe; }
    .chip-factor-purple { background: #ede9fe; color: #5b21b6; border: 1px solid #ddd6fe; }
    .chip-factor-teal   { background: #ccfbf1; color: #115e59; border: 1px solid #99f6e4; }

    /* ── Detail-panel divider heading ────────────────────────── */
    .detail-divider {
        display: flex; align-items: center; gap: 12px;
        margin: 1.5rem 0 0.75rem 0;
    }
    .detail-divider::before, .detail-divider::after {
        content: ""; flex: 1; height: 1px; background: #e2e8f0;
    }
    .detail-divider-text {
        font-size: 0.78rem; font-weight: 700; color: #64748b;
        text-transform: uppercase; letter-spacing: 0.06em;
        white-space: nowrap;
    }
</style>
""")


# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────────────────────
SEED = 20260305
DEPARTMENTS = ["LC 22", "LC NICU", "LC PICU"]
SERVICES = ["Pulmonology", "Cardiac Surgery", "General Surgery", "Neonatology",
            "PICU Intensivist", "ENT", "Neurosurgery"]
HIGH_THRESHOLD = 7
MED_THRESHOLD = 4

STANDARD_ORAL = {"Duoderm", "Cloth tape", "ET tube holder"}
STANDARD_NARE = {"Duoderm", "Tegaderm", "Nare device"}

MOBILITY_TRIGGER = {
    "LC 22": "Ambulatory",
    "LC NICU": "Active / moving in bed",
    "LC PICU": "Ambulatory",
}
MOBILITY_OPTIONS = {
    "LC 22": ["Bedrest", "Dangle", "Chair", "Ambulatory"],
    "LC NICU": ["Minimal movement", "Moderate movement", "Active / moving in bed"],
    "LC PICU": ["Bedrest", "Dangle", "Chair", "Ambulatory"],
}

FIRST_NAMES = [
    "Liam", "Olivia", "Noah", "Emma", "Aiden", "Ava", "Sophia", "Jackson",
    "Lucas", "Mia", "Ethan", "Isabella", "Mason", "Amelia", "Logan",
    "Harper", "Elijah", "Evelyn", "James", "Charlotte", "Benjamin", "Luna",
    "Henry", "Ella", "Sebastian", "Camila", "Mateo", "Aria",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez",
]
RACES = ["White", "Black", "Hispanic", "Asian", "Pacific Islander", "Native American", "Other"]
LANGUAGES = ["English", "Spanish", "Vietnamese", "Arabic", "Mandarin", "Tagalog", "Somali", "Other"]
SECUREMENT_ALL = ["Duoderm", "Cloth tape", "ET tube holder", "Tegaderm", "Nare device",
                  "Silk tape", "Paper tape", "Custom device", "Hydrocolloid"]
ROUTES = ["Oral", "Nasal"]


# ──────────────────────────────────────────────────────────────────────────────
# MOCK DATA GENERATION
# ──────────────────────────────────────────────────────────────────────────────
LOOKBACK_DAYS = 7  # number of prior days of mock data to generate


@st.cache_data
def generate_tool_values(n_per_day: int = 28, days: int = LOOKBACK_DAYS) -> list[dict]:
    """Generate synthetic patient records for today + prior days.

    Patients are mostly stable across days (same MRN/dept/bed) with daily
    variation in clinical values so scores shift realistically.
    """
    today = datetime.date.today()
    rng_base = random.Random(SEED)

    # --- Build a stable patient roster (generated once) ---
    roster = []
    used_mrns = set()
    used_beds: dict[str, set] = {}
    for i in range(n_per_day):
        dept = rng_base.choice(DEPARTMENTS)
        service = rng_base.choice(SERVICES)
        while True:
            mrn = f"MRN{rng_base.randint(100000, 999999)}"
            if mrn not in used_mrns:
                used_mrns.add(mrn)
                break
        if dept not in used_beds:
            used_beds[dept] = set()
        while True:
            bed = f"{rng_base.randint(1, 40):02d}"
            if bed not in used_beds[dept]:
                used_beds[dept].add(bed)
                break
        first = rng_base.choice(FIRST_NAMES)
        last = rng_base.choice(LAST_NAMES)
        route = rng_base.choice(ROUTES)
        age_months = rng_base.randint(0, 216)
        race = rng_base.choice(RACES)
        language = rng_base.choice(LANGUAGES)
        # Stable flags that don't change day-to-day
        ue_history = rng_base.random() < 0.12
        difficult_airway = rng_base.random() < 0.10
        roster.append({
            "patient_id": i, "name": f"{last}, {first}", "mrn": mrn,
            "dept": dept, "bed": bed, "service": service,
            "age_months": age_months, "ett_route": route,
            "race": race, "language": language,
            "ue_history": ue_history, "difficult_airway": difficult_airway,
        })

    # --- Generate daily clinical values for each patient ---
    records = []
    for day_offset in range(days, -1, -1):  # oldest first … today last
        census_date = today - datetime.timedelta(days=day_offset)
        # Per-day RNG seeded from base seed + date ordinal for reproducibility
        rng_day = random.Random(SEED + census_date.toordinal())

        for pat in roster:
            dept = pat["dept"]
            route = pat["ett_route"]
            if rng_day.random() < 0.65:
                std = STANDARD_ORAL if route == "Oral" else STANDARD_NARE
                securement = sorted(std)
            else:
                securement = sorted(rng_day.sample(SECUREMENT_ALL, k=rng_day.randint(1, 3)))

            rec = {
                **pat,
                "census_date": census_date,
                "capd_value": rng_day.choice([4, 5, 6, 7, 8, 9, 10, 11, 12]),
                "emesis_flag": rng_day.random() < 0.18,
                "suction_count": rng_day.randint(0, 12),
                "mobility_level": rng_day.choice(MOBILITY_OPTIONS[dept]),
                "prone_yesterday": rng_day.random() < 0.15,
                "prone_today": rng_day.random() < 0.15,
                "retape_count": rng_day.choice([0, 0, 0, 1, 1, 2, 3]),
                "tube_moved": rng_day.random() < 0.10,
                "sedation_doses_24h": rng_day.choice([0, 0, 1, 2, 3, 4, 5, 6]),
                "weaning_active": rng_day.random() < 0.22,
                "securement_set": securement,
                "ett_depth_cm": rng_day.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14]),
                "visitor_present": rng_day.random() < 0.70,
            }
            records.append(rec)
    return records


# ──────────────────────────────────────────────────────────────────────────────
# SCORING ENGINE — 14 categories
# ──────────────────────────────────────────────────────────────────────────────
def score_capd(tv: dict) -> tuple[int, str]:
    v = tv["capd_value"]
    if v >= 9:
        return 1, f"CAP-D = {v} (>=9)"
    return 0, f"CAP-D = {v}"

def score_emesis(tv: dict) -> tuple[int, str]:
    if tv["emesis_flag"]:
        return 1, "Emesis present"
    if tv["suction_count"] >= 7:
        return 1, f"Suctions = {tv['suction_count']} (>=7)"
    return 0, f"No emesis, suctions = {tv['suction_count']}"

def score_ue_history(tv: dict) -> tuple[int, str]:
    if tv["ue_history"]:
        return 1, "Prior UE within 2 years"
    return 0, "No prior UE"

def score_mobility(tv: dict) -> tuple[int, str]:
    level = tv["mobility_level"]
    trigger = MOBILITY_TRIGGER[tv["dept"]]
    if level == trigger:
        return 1, f"{level} (trigger for {tv['dept']})"
    return 0, f"{level}"

def score_prone(tv: dict) -> tuple[int, str]:
    if tv["prone_yesterday"] or tv["prone_today"]:
        parts = []
        if tv["prone_yesterday"]:
            parts.append("yesterday")
        if tv["prone_today"]:
            parts.append("today")
        return 1, f"Prone {' & '.join(parts)}"
    return 0, "Not prone"

def score_retape(tv: dict) -> tuple[int, str]:
    if tv["retape_count"] >= 2:
        return 1, f"Retapes = {tv['retape_count']} (>=2)"
    if tv["tube_moved"]:
        return 1, "Tube moved"
    return 0, f"Retapes = {tv['retape_count']}, tube stable"

def score_pain_agitation(tv: dict) -> tuple[int, str]:
    return 0, "TBD"

def score_sedation(tv: dict) -> tuple[int, str]:
    d = tv["sedation_doses_24h"]
    if d >= 4:
        return 1, f"Doses = {d} (>=4)"
    return 0, f"Doses = {d}"

def score_weaning(tv: dict) -> tuple[int, str]:
    if tv["weaning_active"]:
        return 1, "Weaning active"
    return 0, "Not weaning"

def score_difficult_airway(tv: dict) -> tuple[int, str]:
    if tv["difficult_airway"]:
        return 1, "Difficult airway flagged"
    return 0, "No difficult airway"

def score_securement(tv: dict) -> tuple[int, str]:
    route = tv["ett_route"]
    s = set(tv["securement_set"])
    std = STANDARD_ORAL if route == "Oral" else STANDARD_NARE
    if s != std:
        return 1, f"Non-standard ({route}): {', '.join(sorted(s))}"
    return 0, f"Standard ({route})"

def score_ett_depth(tv: dict) -> tuple[int, str]:
    d = tv["ett_depth_cm"]
    if d <= 7:
        return 2, f"Depth = {d} cm (<=7, +2)"
    if d <= 9:
        return 1, f"Depth = {d} cm (8-9, +1)"
    return 0, f"Depth = {d} cm"

def score_ethnicity_language(tv: dict) -> tuple[int, str]:
    pts = 0
    parts = []
    if tv["race"] != "White":
        pts += 1
        parts.append(f"Race: {tv['race']}")
    if tv["language"] != "English":
        pts += 1
        parts.append(f"Language: {tv['language']}")
    if pts == 0:
        return 0, "White, English"
    return pts, "; ".join(parts)

def score_social(tv: dict) -> tuple[int, str]:
    if not tv["visitor_present"]:
        return 1, "No visitor present"
    return 0, "Visitor present"


SCORING_CATEGORIES = [
    ("CAP-D", score_capd),
    ("Emesis / Suction", score_emesis),
    ("UE History", score_ue_history),
    ("Mobility", score_mobility),
    ("Prone", score_prone),
    ("Retape / Tube Move", score_retape),
    ("Pain / Agitation", score_pain_agitation),
    ("Sedation", score_sedation),
    ("Weaning", score_weaning),
    ("Difficult Airway", score_difficult_airway),
    ("Securement", score_securement),
    ("ETT Depth", score_ett_depth),
    ("Ethnicity / Language", score_ethnicity_language),
    ("Social / Visitor", score_social),
]


def compute_all_scores(tv: dict) -> dict:
    """Run all scoring functions, return dict with category scores + FinalScore."""
    result = {}
    total = 0
    triggered = []
    for name, fn in SCORING_CATEGORIES:
        pts, reason = fn(tv)
        result[name] = {"pts": pts, "reason": reason}
        total += pts
        if pts > 0 and name != "Pain / Agitation":
            triggered.append(name)
    result["FinalScore"] = total
    result["TriggeredCategories"] = triggered
    return result


def risk_level(score: int) -> str:
    if score >= HIGH_THRESHOLD:
        return "High"
    if score >= MED_THRESHOLD:
        return "Medium"
    return "Low"


@st.cache_data
def build_dataframes() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build the final scored dataframe and the raw tool-values dataframe."""
    records = generate_tool_values()
    rows = []
    for tv in records:
        scores = compute_all_scores(tv)
        final = scores["FinalScore"]
        level = risk_level(final)
        triggered = scores["TriggeredCategories"]
        rows.append({
            "patient_id": tv["patient_id"],
            "census_date": tv["census_date"],
            "name": tv["name"],
            "mrn": tv["mrn"],
            "dept": tv["dept"],
            "bed": tv["bed"],
            "service": tv["service"],
            "score": final,
            "risk": level,
            "triggered": triggered,
            "scores_detail": scores,
        })
    df_final = pd.DataFrame(rows).sort_values(
        ["census_date", "score"], ascending=[False, False]
    ).reset_index(drop=True)
    df_tools = pd.DataFrame(records)
    return df_final, df_tools


# ──────────────────────────────────────────────────────────────────────────────
# HELPER / RENDER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────
def render_kpi(value, label: str, color_class: str, border_class: str) -> str:
    return f"""
    <div class="kpi-card {border_class}">
        <div class="kpi-value {color_class}">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>"""


def risk_badge(level: str) -> str:
    cls = {"High": "sev-high", "Medium": "sev-med", "Low": "sev-low"}
    return f'<span class="{cls.get(level, "sev-low")}">{level}</span>'


def score_cell_html(score: int, level: str) -> str:
    cls = {"High": "score-cell-high", "Medium": "score-cell-med", "Low": "score-cell-low"}
    return f'<span class="{cls.get(level, "score-cell-low")}">{score}</span>'


def indicator_badge(pts: int) -> str:
    if pts >= 2:
        return f'<span class="score-item-pts pts-2">+{pts}</span>'
    if pts >= 1:
        return f'<span class="score-item-pts pts-on">+{pts}</span>'
    return '<span class="score-item-pts pts-off">0</span>'


def dept_badge(dept: str) -> str:
    colors = {"LC 22": "badge-blue", "LC NICU": "badge-orange", "LC PICU": "badge-green"}
    return f'<span class="badge {colors.get(dept, "badge-gray")}">{dept}</span>'


# Map scoring categories to chip color classes for visual variety
_CHIP_COLORS = {
    "CAP-D": "chip-factor-red",
    "Emesis / Suction": "chip-factor-red",
    "UE History": "chip-factor-orange",
    "Mobility": "chip-factor-blue",
    "Prone": "chip-factor-blue",
    "Retape / Tube Move": "chip-factor-orange",
    "Sedation": "chip-factor-purple",
    "Weaning": "chip-factor-purple",
    "Difficult Airway": "chip-factor-red",
    "Securement": "chip-factor-teal",
    "ETT Depth": "chip-factor-red",
    "Ethnicity / Language": "chip-factor-teal",
    "Social / Visitor": "chip-factor-blue",
}


def factor_chip(cat: str) -> str:
    cls = _CHIP_COLORS.get(cat, "chip-factor-red")
    return f'<span class="chip-factor {cls}">{cat}</span>'


def card_risk_class(level: str) -> str:
    """Return card color modifier class based on risk level."""
    return {"High": "card-red", "Medium": "card-orange", "Low": "card-green"}.get(level, "")


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    _logo_path = Path(__file__).parent / "lurie_logo.png"
    st.image(str(_logo_path), width=160)
    st.html("""<div class="sidebar-logo">
        <div class="sidebar-logo-title">UE Risk Scoring</div>
        <div class="sidebar-logo-sub">Pediatric Extubation Risk Monitor</div>
    </div>
    """)

    st.html('<p class="nav-section-label">Filters</p>')

    today = datetime.date.today()
    min_date = today - datetime.timedelta(days=LOOKBACK_DAYS)
    date_filter = st.date_input(
        "Census Date",
        value=today,
        min_value=min_date,
        max_value=today,
    )

    dept_filter = st.selectbox("Department", ["All"] + DEPARTMENTS, index=0)
    service_filter = st.selectbox("Service", ["All"] + SERVICES, index=0)
    risk_filter = st.selectbox("Risk Level", ["All", "High", "Medium", "Low"], index=0)

    st.html("<hr>")
    st.html("""
    <div class="sidebar-version">
        <span class="dot"></span> v1.0.0 &middot; UE Risk Tool
    </div>
    """)


# ──────────────────────────────────────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────────────────────────────────────
df_final, df_tools = build_dataframes()

# Apply filters — date first, then sidebar selectors
df = df_final[df_final["census_date"] == date_filter].copy()
if dept_filter != "All":
    df = df[df["dept"] == dept_filter]
if service_filter != "All":
    df = df[df["service"] == service_filter]
if risk_filter != "All":
    df = df[df["risk"] == risk_filter]


# ──────────────────────────────────────────────────────────────────────────────
# MAIN AREA — Header
# ──────────────────────────────────────────────────────────────────────────────
selected_date_str = date_filter.strftime("%B %d, %Y")
is_today = date_filter == datetime.date.today()
date_badge = "Daily Census" if is_today else "Prior Day"
date_badge_cls = "badge-blue" if is_today else "badge-yellow"
st.html(f"""
<div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:0.5rem;">
    <div>
        <span style="font-size:1.3rem; font-weight:800; color:#1e293b;">
            UE Risk Scoring Tool
        </span>
        <span class="badge {date_badge_cls}" style="margin-left:10px;">{date_badge}</span>
    </div>
    <span style="font-size:0.82rem; color:#64748b; font-weight:500;">{selected_date_str}</span>
</div>
""")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN AREA — KPI Row
# ──────────────────────────────────────────────────────────────────────────────
n_total = len(df)
n_high = len(df[df["risk"] == "High"])
n_med = len(df[df["risk"] == "Medium"])
n_low = len(df[df["risk"] == "Low"])
avg_score = df["score"].mean() if n_total > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.html(render_kpi(n_total, "Total Patients", "primary", "kpi-border-blue"))
with c2:
    st.html(render_kpi(n_high, "High Risk", "urgent", "kpi-border-red"))
with c3:
    st.html(render_kpi(n_med, "Medium Risk", "warn", "kpi-border-orange"))
with c4:
    st.html(render_kpi(n_low, "Low Risk", "ok", "kpi-border-green"))
with c5:
    st.html(render_kpi(f"{avg_score:.1f}", "Avg Score", "", "kpi-border-purple"))


# ──────────────────────────────────────────────────────────────────────────────
# MAIN AREA — Patient Table
# ──────────────────────────────────────────────────────────────────────────────
table_rows = ""
for _, row in df.iterrows():
    # key factors chips (up to 3)
    chips = ""
    for cat in row["triggered"][:3]:
        chips += factor_chip(cat)

    table_rows += f"""
    <tr>
        <td><strong>{row['name']}</strong><br><span style="font-size:0.75rem;color:#94a3b8;">{row['mrn']}</span></td>
        <td>{dept_badge(row['dept'])}</td>
        <td>{row['bed']}</td>
        <td>{row['service']}</td>
        <td>{score_cell_html(row['score'], row['risk'])}</td>
        <td>{risk_badge(row['risk'])}</td>
        <td>{chips if chips else '<span style="color:#cbd5e1;">—</span>'}</td>
    </tr>"""

st.html(f"""
<div class="card">
    <div class="card-header">
        <div class="card-title">Patient Risk Census</div>
        <span class="badge badge-gray">{n_total} patients</span>
    </div>
    <table class="data-table">
        <thead>
            <tr>
                <th>Patient</th>
                <th>Dept</th>
                <th>Bed</th>
                <th>Service</th>
                <th>Score</th>
                <th>Risk</th>
                <th>Key Factors</th>
            </tr>
        </thead>
        <tbody>{table_rows}</tbody>
    </table>
</div>
""")


# ──────────────────────────────────────────────────────────────────────────────
# DRILL-DOWN DETAIL
# ──────────────────────────────────────────────────────────────────────────────
if n_total == 0:
    st.info("No patients match the current filters.")
else:
    # ── Visual divider before drill-down ──
    st.html("""
    <div class="detail-divider">
        <span class="detail-divider-text">Patient Detail</span>
    </div>
    """)

    options = []
    for _, row in df.iterrows():
        risk_icon = {"High": "!!!", "Medium": "!!", "Low": ""}.get(row["risk"], "")
        prefix = f"[{risk_icon}] " if risk_icon else ""
        options.append(
            f"{prefix}{row['name']}  |  {row['dept']}  |  Bed {row['bed']}  |  Score {row['score']}"
        )

    sel_idx = st.selectbox("Select patient for detail view", range(len(options)),
                           format_func=lambda i: options[i], key="detail_select")

    sel_row = df.iloc[sel_idx]
    pid = sel_row["patient_id"]
    tv = df_tools[
        (df_tools["patient_id"] == pid) & (df_tools["census_date"] == date_filter)
    ].iloc[0].to_dict()
    scores_detail = sel_row["scores_detail"]

    col_left, col_right = st.columns([3, 2])

    # ── Left column: patient summary + score breakdown ──
    with col_left:
        # Build score breakdown rows first so we can emit one single st.html block
        breakdown_rows = ""
        max_possible = 16  # theoretical max across all 14 categories
        for cat_name, _ in SCORING_CATEGORIES:
            info = scores_detail[cat_name]
            pts = info["pts"]
            reason = info["reason"]
            row_class = "row-triggered" if pts > 0 else ""
            if cat_name == "Pain / Agitation":
                reason = '<em style="color:#94a3b8;">TBD — scoring not yet implemented</em>'
            breakdown_rows += f"""
                <tr class="{row_class}">
                    <td style="font-weight:600;">{cat_name}</td>
                    <td>{reason}</td>
                    <td style="text-align:center;">{indicator_badge(pts)}</td>
                </tr>"""

        # Total row
        total_score = sel_row["score"]
        breakdown_rows += f"""
                <tr class="row-total">
                    <td>Total</td>
                    <td style="font-size:0.8rem; color:#64748b;">Max possible: {max_possible}</td>
                    <td style="text-align:center;">{score_cell_html(total_score, sel_row['risk'])}</td>
                </tr>"""

        st.html(f"""
        <div class="card {card_risk_class(sel_row['risk'])}">
            <div class="card-header">
                <div class="card-title">{sel_row['name']}</div>
                {risk_badge(sel_row['risk'])}
            </div>
            <div style="display:flex; gap:2rem; margin-bottom:0.75rem; flex-wrap:wrap;">
                <div>
                    <span class="summary-label">MRN</span>
                    <div class="summary-value">{sel_row['mrn']}</div>
                </div>
                <div>
                    <span class="summary-label">Department</span>
                    <div class="summary-value">{sel_row['dept']}</div>
                </div>
                <div>
                    <span class="summary-label">Bed</span>
                    <div class="summary-value">{sel_row['bed']}</div>
                </div>
                <div>
                    <span class="summary-label">Service</span>
                    <div class="summary-value">{sel_row['service']}</div>
                </div>
                <div>
                    <span class="summary-label">Final Score</span>
                    <div class="summary-value">{score_cell_html(sel_row['score'], sel_row['risk'])}</div>
                </div>
            </div>
            <div class="detail-section-label">Score Breakdown</div>
            <table class="data-table" style="margin-top:0.25rem;">
                <thead>
                    <tr><th>Category</th><th>Detail</th><th style="text-align:center;">Pts</th></tr>
                </thead>
                <tbody>
                {breakdown_rows}
                </tbody>
            </table>
        </div>
        """)

    # ── Right column: raw tool values ──
    with col_right:
        age_m = tv["age_months"]
        age_str = f"{age_m // 12}y {age_m % 12}m" if age_m >= 12 else f"{age_m}m"

        def sv(label, value):
            return f'<div><span class="summary-label">{label}</span><div class="summary-value">{value}</div></div>'

        st.html(f"""
        <div class="card {card_risk_class(sel_row['risk'])}">
            <div class="card-header">
                <div class="card-title">Tool Values</div>
                {dept_badge(sel_row['dept'])}
            </div>

            <div class="detail-section-label">Demographics</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Age", age_str)}
                {sv("Race", tv["race"])}
                {sv("Language", tv["language"])}
                {sv("Visitor Present", "Yes" if tv["visitor_present"] else "No")}
            </div>

            <div class="detail-section-label">CAP-D Data</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("CAP-D Score", tv["capd_value"])}
            </div>

            <div class="detail-section-label">Emesis / Suction</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Emesis", "Yes" if tv["emesis_flag"] else "No")}
                {sv("Suction Count", tv["suction_count"])}
            </div>

            <div class="detail-section-label">UE History</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Prior UE (2yr)", "Yes" if tv["ue_history"] else "No")}
            </div>

            <div class="detail-section-label">Mobility</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Mobility Level", tv["mobility_level"])}
                {sv("Dept Trigger", MOBILITY_TRIGGER[tv["dept"]])}
            </div>

            <div class="detail-section-label">Prone / Retape</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Prone Yesterday", "Yes" if tv["prone_yesterday"] else "No")}
                {sv("Prone Today", "Yes" if tv["prone_today"] else "No")}
                {sv("Retape Count", tv["retape_count"])}
                {sv("Tube Moved", "Yes" if tv["tube_moved"] else "No")}
            </div>

            <div class="detail-section-label">Sedation / Weaning</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Sedation Doses (24h)", tv["sedation_doses_24h"])}
                {sv("Weaning Active", "Yes" if tv["weaning_active"] else "No")}
            </div>

            <div class="detail-section-label">Airway / Securement</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Difficult Airway", "Yes" if tv["difficult_airway"] else "No")}
                {sv("ETT Route", tv["ett_route"])}
                {sv("Securement", ", ".join(tv["securement_set"]))}
            </div>

            <div class="detail-section-label">ETT Depth</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:0 1rem;">
                {sv("Depth (cm)", tv["ett_depth_cm"])}
            </div>
        </div>
        """)
