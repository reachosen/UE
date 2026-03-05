"""
Safety Intelligence Dashboard — Streamlit Application
======================================================
AI-powered patient safety event analysis, routing, and trend monitoring.
Same skin/styling as the NAKI Review app.

Run:  streamlit run safety_dashboard.py
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
    page_title="Safety Intelligence Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — matching NAKI skin
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
    /* Collapse default gap between every sidebar element */
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
    /* Remove extra padding from st.html blocks inside sidebar */
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
    /* Make KPI columns equal height */
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

    /* ── Gap / problem dots ────────────────────────────────────── */
    .dot-red { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #E53935; margin-right: 6px; }
    .dot-orange { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #FB8C00; margin-right: 6px; }
    .dot-green { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #43A047; margin-right: 6px; }
    .dot-blue { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #1E88E5; margin-right: 6px; }

    /* ── Filter bar ────────────────────────────────────────────── */
    .filter-bar {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 1.25rem;
    }

    /* ── Urgency labels ────────────────────────────────────────── */
    .urgency-imm { color: #991b1b; font-weight: 700; }
    .urgency-urg { color: #E53935; font-weight: 700; }
    .urgency-high { color: #FB8C00; font-weight: 700; }
    .urgency-med { color: #64748b; font-weight: 600; }

    /* ── Completeness score ring ─────────────────────────────── */
    .score-ring {
        width: 72px; height: 72px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; font-weight: 800; color: #1e293b;
        margin: 0 auto 6px auto;
    }
    .score-high {
        background: conic-gradient(#43A047 calc(var(--pct) * 1%), #e2e8f0 0);
        box-shadow: inset 0 0 0 10px #fff;
    }
    .score-med {
        background: conic-gradient(#FB8C00 calc(var(--pct) * 1%), #e2e8f0 0);
        box-shadow: inset 0 0 0 10px #fff;
    }
    .score-low {
        background: conic-gradient(#E53935 calc(var(--pct) * 1%), #e2e8f0 0);
        box-shadow: inset 0 0 0 10px #fff;
    }

    /* ── Checklist items ─────────────────────────────────────── */
    .check-item {
        display: flex; align-items: center; gap: 8px;
        padding: 5px 0; font-size: 0.85rem; color: #334155;
    }
    .check-done::before {
        content: "\2713"; font-weight: 700; color: #43A047;
        width: 20px; height: 20px; display: inline-flex;
        align-items: center; justify-content: center;
        background: #dcfce7; border-radius: 50%; font-size: 0.72rem;
        flex-shrink: 0;
    }
    .check-miss::before {
        content: "\2717"; font-weight: 700; color: #E53935;
        width: 20px; height: 20px; display: inline-flex;
        align-items: center; justify-content: center;
        background: #fee2e2; border-radius: 50%; font-size: 0.72rem;
        flex-shrink: 0;
    }

    /* hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""")


# ──────────────────────────────────────────────────────────────────────────────
# MOCK DATA — DIA_GOLD_AI.RLDATIX.*
# ──────────────────────────────────────────────────────────────────────────────

def get_weekly_digest(events=None, escalations=None):
    """V_WEEKLY_DIGEST mock — computes from filtered data when provided"""
    if events is None:
        return {
            "events_analyzed": 48,
            "problems_found": 159,
            "high_severity": 26,
            "urgent_escalations": 22,
            "routing_alerts": 6,
        }
    problems = sum(e.get("problems", 0) for e in events)
    high_sev = sum(1 for e in events if e.get("severity", "").lower() == "high")
    esc_count = len(escalations) if escalations else 0
    return {
        "events_analyzed": len(events),
        "problems_found": problems,
        "high_severity": high_sev,
        "urgent_escalations": esc_count,
        "routing_alerts": 6,
    }


def get_location_risk(events=None):
    """V_LOCATION_RISK_SCORE mock — recomputes from filtered events when provided"""
    _default = [
        {"location": "2nd Floor – Cardiac ICU", "risk_score": 92, "events": 8, "level": "HIGH"},
        {"location": "16th Floor – Surgical", "risk_score": 87, "events": 7, "level": "HIGH"},
        {"location": "17th Floor – Oncology", "risk_score": 81, "events": 6, "level": "HIGH"},
        {"location": "7th Floor – General Med", "risk_score": 68, "events": 5, "level": "MEDIUM"},
        {"location": "18th Floor – Rehab", "risk_score": 55, "events": 3, "level": "MEDIUM"},
        {"location": "3rd Floor – Pediatrics", "risk_score": 34, "events": 2, "level": "LOW"},
        {"location": "5th Floor – NICU", "risk_score": 28, "events": 1, "level": "LOW"},
    ]
    if events is None:
        return _default
    total_all = 6  # total unfiltered events
    total_filtered = len(events)
    if total_filtered == 0:
        return []
    ratio = total_filtered / total_all
    result = []
    for loc in _default:
        scaled_score = max(1, int(loc["risk_score"] * ratio))
        scaled_events = max(0, int(loc["events"] * ratio))
        level = "HIGH" if scaled_score >= 75 else "MEDIUM" if scaled_score >= 40 else "LOW"
        result.append({"location": loc["location"], "risk_score": scaled_score, "events": scaled_events, "level": level})
    return [r for r in result if r["events"] > 0]


def get_escalation_queue():
    """V_ESCALATION_QUEUE mock"""
    return [
        {"file_id": "54117", "event_type": "IV/Vascular Access", "location": "16th Floor",
         "urgency": "IMMEDIATE", "reason": "Harm event – central line infection, patient transferred to ICU",
         "date": "Dec 26", "severity": "High", "date_obj": datetime.date(2025, 12, 26)},
        {"file_id": "53795", "event_type": "Nutrition/Feeding", "location": "17th Floor",
         "urgency": "URGENT", "reason": "Systemic gap – 3rd NPO violation this quarter, same unit",
         "date": "Dec 18", "severity": "High", "date_obj": datetime.date(2025, 12, 18)},
        {"file_id": "54092", "event_type": "Medication Error", "location": "2nd Floor",
         "urgency": "URGENT", "reason": "Wrong dose administered – 10x overdose caught by pharmacy",
         "date": "Dec 24", "severity": "High", "date_obj": datetime.date(2025, 12, 24)},
        {"file_id": "53988", "event_type": "Fall", "location": "7th Floor",
         "urgency": "HIGH", "reason": "Repeat fall – same patient, 2nd event in 72 hours",
         "date": "Dec 21", "severity": "Medium", "date_obj": datetime.date(2025, 12, 21)},
        {"file_id": "53901", "event_type": "Skin Integrity", "location": "18th Floor",
         "urgency": "HIGH", "reason": "Stage 3 pressure injury, documentation gaps in turning schedule",
         "date": "Dec 19", "severity": "Medium", "date_obj": datetime.date(2025, 12, 19)},
    ]


def get_category_summary(events=None):
    """V_ACTION_CATEGORY_SUMMARY mock — computes from filtered events when provided"""
    if events is None:
        return [
            {"category": "Process/Procedure", "count": 89, "pct": 56},
            {"category": "Equipment/Device", "count": 25, "pct": 16},
            {"category": "Communication", "count": 18, "pct": 11},
            {"category": "Documentation", "count": 14, "pct": 9},
            {"category": "Training/Education", "count": 8, "pct": 5},
            {"category": "Environment", "count": 5, "pct": 3},
        ]
    # Map problem categories to summary categories
    cat_map = {
        "Process": "Process/Procedure", "Equipment": "Equipment/Device",
        "Communication": "Communication", "Documentation": "Documentation",
        "Training": "Training/Education",
    }
    counts = {}
    for e in events:
        for p in e.get("problems_detail", []):
            cat = cat_map.get(p.get("category", ""), p.get("category", "Other"))
            counts[cat] = counts.get(cat, 0) + 1
    total = max(sum(counts.values()), 1)
    result = [{"category": k, "count": v, "pct": int(round(v / total * 100))} for k, v in counts.items()]
    result.sort(key=lambda x: x["count"], reverse=True)
    return result


def get_clinical_category_summary(events=None):
    """V_CLINICAL_CATEGORY_SPOTLIGHT mock — top clinical PRIMARY categories by event type"""
    base = {
        "IV/Vascular Access": {
            "color": "#FF9800",
            "categories": [
                {"category": "CLABSI", "count": 12, "pct": 31},
                {"category": "Infiltration/Extravasation", "count": 9, "pct": 23},
                {"category": "Line Dislodgement", "count": 8, "pct": 21},
                {"category": "Access Difficulty", "count": 5, "pct": 13},
            ],
        },
        "Medication Error": {
            "color": "#9C27B0",
            "categories": [
                {"category": "Weight-Based Dosing Error", "count": 11, "pct": 30},
                {"category": "Wrong Medication", "count": 8, "pct": 22},
                {"category": "Omitted Dose", "count": 6, "pct": 16},
                {"category": "Wrong Route", "count": 4, "pct": 11},
            ],
        },
        "Nutrition/Feeding": {
            "color": "#2196F3",
            "categories": [
                {"category": "NPO Violation", "count": 10, "pct": 29},
                {"category": "Wrong Diet Delivered", "count": 7, "pct": 20},
                {"category": "Feeding Tube Issue", "count": 6, "pct": 17},
                {"category": "Allergy Miss", "count": 4, "pct": 11},
            ],
        },
        "Fall": {
            "color": "#009688",
            "categories": [
                {"category": "Unassisted Fall", "count": 8, "pct": 36},
                {"category": "Bed Exit", "count": 6, "pct": 27},
                {"category": "Transfer Fall", "count": 4, "pct": 18},
            ],
        },
        "Skin Integrity": {
            "color": "#F44336",
            "categories": [
                {"category": "Pressure Injury", "count": 7, "pct": 35},
                {"category": "Skin Tear", "count": 5, "pct": 25},
                {"category": "Wound Care Delay", "count": 4, "pct": 20},
            ],
        },
    }
    if events is None:
        return base
    # Filter-aware: scale counts by event-type ratio
    type_counts = {}
    for e in events:
        et = e.get("event_type", "")
        type_counts[et] = type_counts.get(et, 0) + 1
    result = {}
    for et, data in base.items():
        if type_counts.get(et, 0) == 0:
            continue
        ratio = type_counts[et] / max(sum(type_counts.values()), 1)
        scaled = []
        for c in data["categories"]:
            sc = max(1, int(round(c["count"] * ratio * len(events) / 10)))
            scaled.append({"category": c["category"], "count": sc, "pct": c["pct"]})
        result[et] = {"color": data["color"], "categories": scaled}
    return result


def get_event_list():
    """V_SAFETY_CLINICAL_REVIEW mock"""
    return [
        {"file_id": "53801", "event_type": "Nutrition/Feeding", "date": "Dec 15",
         "date_obj": datetime.date(2025, 12, 15),
         "location": "7th Floor", "problems": 4, "gaps": 2, "severity": "High",
         "status": "Under Review",
         "datix_general": "Nutrition/Diet", "datix_specific": "NPO Violation",
         "narrative": "Patient received in PACU after ENT surgery. Diet orders conflicting – NPO vs clear liquids. Patient given apple juice by aide before orders clarified. No aspiration event, but protocol violation identified.",
         "problems_detail": [
             {"problem": "Conflicting diet orders between ENT and anesthesia", "category": "Communication"},
             {"problem": "Diet status not discussed during PACU handoff", "category": "Communication"},
             {"problem": "Patient given juice despite NPO status", "category": "Process"},
             {"problem": "No visual NPO flagging at bedside", "category": "Documentation"},
         ],
         "suggested_actions": ["EHR hard-stop alert for conflicting diet orders", "PACU handoff protocol update", "Visual NPO flagging system", "Diet order reconciliation workflow"],
         "actual_followups": [
             {"action": "Chart reviewed by charge nurse", "type": "Investigation"},
             {"action": "ENT and anesthesia teams notified", "type": "Escalation"},
             {"action": "NPO status clarified in EHR", "type": "Documentation"},
         ],
         "gaps_detail": ["No EHR alert implementation planned", "No formal handoff protocol update initiated"]},
        {"file_id": "54117", "event_type": "IV/Vascular Access", "date": "Dec 26",
         "date_obj": datetime.date(2025, 12, 26),
         "location": "16th Floor", "problems": 3, "gaps": 1, "severity": "High",
         "status": "Escalated",
         "datix_general": "Equipment/Medical Device", "datix_specific": "Line Infection",
         "narrative": "Central line infection identified 48 hours post-insertion. Patient developed sepsis, transferred to ICU. Line inserted by resident without attending supervision during night shift.",
         "problems_detail": [
             {"problem": "Central line inserted without attending supervision", "category": "Process"},
             {"problem": "Sterile technique breach not documented", "category": "Documentation"},
             {"problem": "Post-insertion monitoring checklist incomplete", "category": "Process"},
         ],
         "suggested_actions": ["Mandatory attending supervision for central lines", "Real-time sterile technique audit", "Automated post-insertion monitoring alerts"],
         "actual_followups": [
             {"action": "Infection control notified", "type": "Escalation"},
             {"action": "Root cause analysis initiated", "type": "Investigation"},
         ],
         "gaps_detail": ["Supervision policy not yet updated"]},
        {"file_id": "54092", "event_type": "Medication Error", "date": "Dec 24",
         "date_obj": datetime.date(2025, 12, 24),
         "location": "2nd Floor", "problems": 2, "gaps": 1, "severity": "High",
         "status": "Under Review",
         "datix_general": "Medication", "datix_specific": "Wrong Dose",
         "narrative": "10x overdose of heparin ordered for pediatric patient. Caught by pharmacist during verification. No harm to patient. Order entry system did not flag weight-based dosing error.",
         "problems_detail": [
             {"problem": "Weight-based dosing calculation error", "category": "Process"},
             {"problem": "EHR dose range check not configured for pediatric heparin", "category": "Equipment"},
         ],
         "suggested_actions": ["Configure pediatric heparin dose range alerts", "Mandatory weight verification before high-risk meds"],
         "actual_followups": [
             {"action": "Pharmacy alert escalated to IT", "type": "Escalation"},
         ],
         "gaps_detail": ["EHR configuration change not yet scheduled"]},
        {"file_id": "53988", "event_type": "Fall", "date": "Dec 21",
         "date_obj": datetime.date(2025, 12, 21),
         "location": "7th Floor", "problems": 2, "gaps": 0, "severity": "Medium",
         "status": "Closed",
         "datix_general": "Patient Accident", "datix_specific": "Fall",
         "narrative": "Patient fall in bathroom, second fall in 72 hours. Bed alarm was active. Patient attempted independent ambulation against care plan. Minor bruising, no fracture.",
         "problems_detail": [
             {"problem": "Patient non-compliance with fall precautions", "category": "Communication"},
             {"problem": "Staffing ratio limited 1:1 monitoring", "category": "Process"},
         ],
         "suggested_actions": ["1:1 sitter assignment", "Family education on fall risk"],
         "actual_followups": [
             {"action": "Fall risk reassessment completed", "type": "Investigation"},
             {"action": "Family meeting conducted", "type": "Documentation"},
         ],
         "gaps_detail": []},
        {"file_id": "53901", "event_type": "Skin Integrity", "date": "Dec 19",
         "date_obj": datetime.date(2025, 12, 19),
         "location": "18th Floor", "problems": 3, "gaps": 2, "severity": "Medium",
         "status": "Under Review",
         "datix_general": "Clinical Treatment", "datix_specific": "Pressure Injury",
         "narrative": "Stage 3 pressure injury discovered during wound care assessment. Turning schedule documentation incomplete for prior 48 hours. Wound care consult delayed by 24 hours.",
         "problems_detail": [
             {"problem": "Turning schedule not followed per protocol", "category": "Process"},
             {"problem": "Wound care consult delay", "category": "Communication"},
             {"problem": "Incomplete skin assessment documentation", "category": "Documentation"},
         ],
         "suggested_actions": ["Automated turning reminders", "Wound care consult escalation path", "Skin assessment audit"],
         "actual_followups": [
             {"action": "Wound care team consulted", "type": "Investigation"},
         ],
         "gaps_detail": ["Turning schedule system not implemented", "No audit process initiated"]},
        {"file_id": "53724", "event_type": "IV/Vascular Access", "date": "Dec 12",
         "date_obj": datetime.date(2025, 12, 12),
         "location": "18th Floor", "problems": 2, "gaps": 1, "severity": "Medium",
         "status": "Under Review",
         "datix_general": "Equipment/Medical Device", "datix_specific": "Dislodgement",
         "narrative": "PICC line dislodgement during patient transport. Line not secured per protocol. Required re-insertion in interventional radiology.",
         "problems_detail": [
             {"problem": "PICC line not secured per transport protocol", "category": "Process"},
             {"problem": "Transport team not trained on line management", "category": "Training"},
         ],
         "suggested_actions": ["Transport team line management training", "Pre-transport line security checklist"],
         "actual_followups": [
             {"action": "Incident documented", "type": "Documentation"},
         ],
         "gaps_detail": ["Training program not yet developed"]},
    ]


def get_routing_alerts():
    """V_ROUTING_ALERTS mock"""
    return [
        {"department": "VAT (Vascular Access Team)", "events_missing": 31, "level": "HIGH",
         "description": "IV/Vascular events not routed to VAT for specialized review",
         "event_types": ["IV/Vascular Access"]},
        {"department": "Food Services", "events_missing": 15, "level": "HIGH",
         "description": "Nutrition events lack Food Services department tag",
         "event_types": ["Nutrition/Feeding"]},
        {"department": "Pharmacy", "events_missing": 6, "level": "MEDIUM",
         "description": "Medication events missing pharmacy co-review assignment",
         "event_types": ["Medication Error"]},
        {"department": "Eating Disorder Unit", "events_missing": 2, "level": "LOW",
         "description": "Nutrition events for ED patients not flagged for specialized unit",
         "event_types": ["Nutrition/Feeding"]},
        {"department": "Infection Control", "events_missing": 4, "level": "MEDIUM",
         "description": "Central line infections not auto-routed to IC team",
         "event_types": ["IV/Vascular Access"]},
    ]


def get_routing_action_items():
    """V_ROUTING_ACTION_ITEMS mock"""
    return [
        {"file_id": "53801", "reported_to": "7th Floor", "should_be": "PACU",
         "must_tag": "Food Services", "priority": "URGENT",
         "date_obj": datetime.date(2025, 12, 15), "event_type": "Nutrition/Feeding"},
        {"file_id": "53724", "reported_to": "18th Floor", "should_be": "Oncology Clinic",
         "must_tag": "VAT, Pharmacy", "priority": "URGENT",
         "date_obj": datetime.date(2025, 12, 12), "event_type": "IV/Vascular Access"},
        {"file_id": "54117", "reported_to": "16th Floor", "should_be": "16th Floor",
         "must_tag": "Infection Control, VAT", "priority": "HIGH",
         "date_obj": datetime.date(2025, 12, 26), "event_type": "IV/Vascular Access"},
        {"file_id": "54092", "reported_to": "2nd Floor", "should_be": "2nd Floor",
         "must_tag": "Pharmacy", "priority": "HIGH",
         "date_obj": datetime.date(2025, 12, 24), "event_type": "Medication Error"},
        {"file_id": "53901", "reported_to": "18th Floor", "should_be": "18th Floor",
         "must_tag": "Wound Care", "priority": "MEDIUM",
         "date_obj": datetime.date(2025, 12, 19), "event_type": "Skin Integrity"},
    ]


def get_root_cause_trends(events=None, period="Weekly"):
    """DEPRECATED — V_ROOT_CAUSE_TRENDS mock — scales by filter ratio when events provided.
    Replaced by get_event_type_time_trends(). Kept as fallback."""
    if period == "Weekly":
        base = {
            "Period": [f"Week {i}" for i in range(1, 11)],
            "Process":       [32, 41, 48, 38, 35, 44, 50, 42, 37, 46],
            "Communication": [18, 22, 15, 20, 17, 24, 19, 21, 16, 23],
            "Equipment":     [8, 12, 14, 10, 9, 13, 15, 11, 10, 12],
            "Documentation": [6, 9, 11, 8, 7, 10, 12, 9, 8, 11],
        }
    elif period == "Monthly":
        base = {
            "Period": [f"Month {i}" for i in range(1, 11)],
            "Process":       [128, 164, 192, 152, 140, 176, 200, 168, 148, 184],
            "Communication": [72, 88, 60, 80, 68, 96, 76, 84, 64, 92],
            "Equipment":     [32, 48, 56, 40, 36, 52, 60, 44, 40, 48],
            "Documentation": [24, 36, 44, 32, 28, 40, 48, 36, 32, 44],
        }
    else:  # Quarterly
        base = {
            "Period": [f"Q{i}" for i in range(1, 7)],
            "Process":       [484, 544, 576, 524, 504, 560],
            "Communication": [240, 268, 236, 264, 248, 280],
            "Equipment":     [136, 156, 148, 140, 144, 160],
            "Documentation": [104, 120, 116, 108, 112, 128],
        }
    if events is not None:
        ratio = len(events) / 6  # 6 = total unfiltered events
        for key in ["Process", "Communication", "Equipment", "Documentation"]:
            base[key] = [max(0, int(v * ratio)) for v in base[key]]
    return pd.DataFrame(base)


def get_event_type_time_trends(events=None, period="Weekly"):
    """Time-series for Event Types (Primary Categories) view across periods. Scales by filter ratio."""
    if period == "Weekly":
        labels = [f"Week {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "Nutrition / Feeding":   [14, 18, 21, 16, 15, 19, 22, 18, 16, 20],
            "IV / Vascular Access":  [11, 14, 16, 13, 12, 15, 17, 14, 12, 16],
            "Medication Error":      [10, 12, 14, 11, 10, 13, 15, 12, 10, 14],
            "Fall":                  [6, 8, 9, 7, 6, 8, 10, 8, 7, 9],
            "Skin Integrity":        [5, 7, 8, 6, 5, 7, 8, 7, 6, 7],
            "Documentation Gap":     [5, 6, 7, 5, 4, 6, 8, 6, 5, 7],
        }
    elif period == "Monthly":
        labels = [f"Month {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "Nutrition / Feeding":   [56, 72, 84, 64, 60, 76, 88, 72, 64, 80],
            "IV / Vascular Access":  [44, 56, 64, 52, 48, 60, 68, 56, 48, 64],
            "Medication Error":      [40, 48, 56, 44, 40, 52, 60, 48, 40, 56],
            "Fall":                  [24, 32, 36, 28, 24, 32, 40, 32, 28, 36],
            "Skin Integrity":        [20, 28, 32, 24, 20, 28, 32, 28, 24, 28],
            "Documentation Gap":     [20, 24, 28, 20, 16, 24, 32, 24, 20, 28],
        }
    else:  # Quarterly
        labels = [f"Q{i}" for i in range(1, 7)]
        data = {
            "Period": labels,
            "Nutrition / Feeding":   [212, 240, 264, 248, 228, 256],
            "IV / Vascular Access":  [168, 188, 208, 196, 180, 200],
            "Medication Error":      [148, 168, 184, 172, 160, 180],
            "Fall":                  [92, 104, 112, 108, 100, 112],
            "Skin Integrity":        [76, 88, 96, 92, 84, 92],
            "Documentation Gap":     [68, 80, 88, 80, 76, 84],
        }
    cats = [c for c in data if c != "Period"]
    if events is not None:
        ratio = len(events) / 6
        for key in cats:
            data[key] = [max(0, int(v * ratio)) for v in data[key]]
    return pd.DataFrame(data)


def get_clinical_subcategory_time_trends(events=None, period="Weekly"):
    """Time-series for Clinical Subcategories view across periods. Scales by filter ratio."""
    if period == "Weekly":
        labels = [f"Week {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            # IV/Vascular Access subcategories
            "CLABSI":                      [4, 5, 6, 4, 5, 6, 7, 5, 4, 6],
            "Infiltration/Extravasation":  [3, 4, 4, 3, 3, 4, 5, 4, 3, 4],
            "Line Dislodgement":           [2, 3, 4, 3, 2, 3, 3, 3, 3, 4],
            "Access Difficulty":           [2, 2, 2, 3, 2, 2, 2, 2, 2, 2],
            # Medication Error subcategories
            "Weight-Based Dosing Error":   [3, 4, 5, 3, 3, 4, 5, 4, 3, 5],
            "Wrong Medication":            [2, 3, 3, 3, 2, 3, 4, 3, 3, 3],
            "Omitted Dose":                [2, 2, 3, 2, 2, 3, 3, 2, 2, 3],
            "Wrong Route":                 [1, 2, 2, 2, 1, 2, 2, 2, 1, 2],
            # Nutrition/Feeding subcategories
            "NPO Violation":               [4, 5, 6, 5, 4, 5, 7, 5, 5, 6],
            "Wrong Diet Delivered":         [3, 4, 4, 3, 3, 4, 4, 4, 3, 4],
            "Feeding Tube Issue":          [3, 3, 4, 3, 3, 4, 4, 3, 3, 4],
            "Allergy Miss":                [2, 2, 3, 2, 2, 2, 3, 2, 2, 2],
            # Fall subcategories
            "Unassisted Fall":             [3, 3, 4, 3, 3, 4, 4, 3, 3, 4],
            "Bed Exit":                    [2, 3, 3, 2, 2, 2, 3, 3, 2, 3],
            "Transfer Fall":               [1, 2, 2, 2, 1, 2, 3, 2, 2, 2],
            # Skin Integrity subcategories
            "Pressure Injury":             [2, 3, 3, 2, 2, 3, 3, 3, 2, 3],
            "Skin Tear":                   [2, 2, 3, 2, 2, 2, 3, 2, 2, 2],
            "Wound Care Delay":            [1, 2, 2, 2, 1, 2, 2, 2, 2, 2],
        }
    elif period == "Monthly":
        labels = [f"Month {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "CLABSI":                      [16, 20, 24, 16, 20, 24, 28, 20, 16, 24],
            "Infiltration/Extravasation":  [12, 16, 16, 12, 12, 16, 20, 16, 12, 16],
            "Line Dislodgement":           [8, 12, 16, 12, 8, 12, 12, 12, 12, 16],
            "Access Difficulty":           [8, 8, 8, 12, 8, 8, 8, 8, 8, 8],
            "Weight-Based Dosing Error":   [12, 16, 20, 12, 12, 16, 20, 16, 12, 20],
            "Wrong Medication":            [8, 12, 12, 12, 8, 12, 16, 12, 12, 12],
            "Omitted Dose":                [8, 8, 12, 8, 8, 12, 12, 8, 8, 12],
            "Wrong Route":                 [4, 8, 8, 8, 4, 8, 8, 8, 4, 8],
            "NPO Violation":               [16, 20, 24, 20, 16, 20, 28, 20, 20, 24],
            "Wrong Diet Delivered":         [12, 16, 16, 12, 12, 16, 16, 16, 12, 16],
            "Feeding Tube Issue":          [12, 12, 16, 12, 12, 16, 16, 12, 12, 16],
            "Allergy Miss":                [8, 8, 12, 8, 8, 8, 12, 8, 8, 8],
            "Unassisted Fall":             [12, 12, 16, 12, 12, 16, 16, 12, 12, 16],
            "Bed Exit":                    [8, 12, 12, 8, 8, 8, 12, 12, 8, 12],
            "Transfer Fall":               [4, 8, 8, 8, 4, 8, 12, 8, 8, 8],
            "Pressure Injury":             [8, 12, 12, 8, 8, 12, 12, 12, 8, 12],
            "Skin Tear":                   [8, 8, 12, 8, 8, 8, 12, 8, 8, 8],
            "Wound Care Delay":            [4, 8, 8, 8, 4, 8, 8, 8, 8, 8],
        }
    else:  # Quarterly
        labels = [f"Q{i}" for i in range(1, 7)]
        data = {
            "Period": labels,
            "CLABSI":                      [60, 68, 76, 72, 64, 76],
            "Infiltration/Extravasation":  [48, 52, 60, 56, 48, 56],
            "Line Dislodgement":           [36, 44, 48, 44, 40, 48],
            "Access Difficulty":           [24, 28, 28, 28, 28, 28],
            "Weight-Based Dosing Error":   [48, 56, 64, 60, 52, 64],
            "Wrong Medication":            [36, 44, 48, 44, 40, 48],
            "Omitted Dose":                [28, 32, 40, 36, 32, 40],
            "Wrong Route":                 [20, 24, 28, 24, 20, 28],
            "NPO Violation":               [60, 68, 80, 72, 64, 80],
            "Wrong Diet Delivered":         [44, 52, 56, 52, 48, 56],
            "Feeding Tube Issue":          [40, 44, 52, 48, 44, 52],
            "Allergy Miss":                [28, 28, 36, 32, 28, 32],
            "Unassisted Fall":             [40, 44, 52, 48, 44, 52],
            "Bed Exit":                    [28, 36, 40, 36, 32, 40],
            "Transfer Fall":               [20, 28, 32, 28, 24, 32],
            "Pressure Injury":             [28, 36, 40, 36, 32, 40],
            "Skin Tear":                   [24, 28, 36, 32, 28, 32],
            "Wound Care Delay":            [16, 24, 28, 24, 24, 28],
        }
    cats = [c for c in data if c != "Period"]
    if events is not None:
        ratio = len(events) / 6
        for key in cats:
            data[key] = [max(0, int(v * ratio)) for v in data[key]]
    return pd.DataFrame(data)


def get_root_cause_distribution(events=None):
    """V_ROOT_CAUSE_TRENDS aggregate mock — scales by filter ratio when events provided"""
    base = [
        {"cause": "System Gap", "pct": 47},
        {"cause": "Human Error", "pct": 25},
        {"cause": "Handoff Failure", "pct": 21},
        {"cause": "Knowledge Gap", "pct": 4},
        {"cause": "Other", "pct": 3},
    ]
    if events is not None and len(events) < 6:
        ratio = len(events) / 6
        for item in base:
            item["pct"] = max(1, int(item["pct"] * ratio))
    return base


def get_cross_cutting(events=None):
    """V_CATEGORY_MONITORING mock — scales by filter ratio when events provided"""
    base = [
        {"pair": "Process + System Gap", "count": 34, "trend": "Increasing"},
        {"pair": "Communication + Handoff Failure", "count": 19, "trend": "Stable"},
        {"pair": "Equipment + Human Error", "count": 12, "trend": "Decreasing"},
        {"pair": "Documentation + System Gap", "count": 8, "trend": "Increasing"},
    ]
    if events is not None and len(events) < 6:
        ratio = len(events) / 6
        for item in base:
            item["count"] = max(0, int(item["count"] * ratio))
    return base


def get_action_trends(events=None):
    """V_ACTION_TRENDS mock — scales by filter ratio when events provided"""
    base = [
        {"action_type": "Investigation", "pct": 30},
        {"action_type": "Documentation", "pct": 23},
        {"action_type": "Education/Training", "pct": 15},
        {"action_type": "Escalation", "pct": 14},
        {"action_type": "Policy Update", "pct": 10},
        {"action_type": "System Change", "pct": 8},
    ]
    if events is not None and len(events) < 6:
        ratio = len(events) / 6
        for item in base:
            item["pct"] = max(1, int(item["pct"] * ratio))
    return base


def get_root_cause_time_trends(events=None, period="Weekly"):
    """Time-series for Root Causes view across periods. Scales by filter ratio."""
    if period == "Weekly":
        labels = [f"Week {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "System Gap":      [18, 22, 25, 20, 28, 24, 30, 26, 22, 27],
            "Human Error":     [10, 12, 9, 14, 11, 13, 10, 15, 12, 11],
            "Handoff Failure": [8, 10, 12, 9, 11, 14, 10, 8, 13, 11],
            "Knowledge Gap":   [3, 2, 4, 3, 5, 2, 4, 3, 2, 4],
            "Other":           [2, 1, 3, 2, 1, 2, 3, 1, 2, 2],
        }
    elif period == "Monthly":
        labels = [f"Month {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "System Gap":      [72, 88, 100, 80, 112, 96, 120, 104, 88, 108],
            "Human Error":     [40, 48, 36, 56, 44, 52, 40, 60, 48, 44],
            "Handoff Failure": [32, 40, 48, 36, 44, 56, 40, 32, 52, 44],
            "Knowledge Gap":   [12, 8, 16, 12, 20, 8, 16, 12, 8, 16],
            "Other":           [8, 4, 12, 8, 4, 8, 12, 4, 8, 8],
        }
    else:  # Quarterly
        labels = [f"Q{i}" for i in range(1, 7)]
        data = {
            "Period": labels,
            "System Gap":      [260, 288, 336, 320, 296, 348],
            "Human Error":     [124, 148, 132, 156, 144, 140],
            "Handoff Failure": [120, 136, 152, 128, 148, 140],
            "Knowledge Gap":   [36, 44, 32, 48, 36, 40],
            "Other":           [24, 16, 28, 20, 16, 24],
        }
    if events is not None:
        ratio = len(events) / 6
        for key in ["System Gap", "Human Error", "Handoff Failure", "Knowledge Gap", "Other"]:
            data[key] = [max(0, int(v * ratio)) for v in data[key]]
    return pd.DataFrame(data)


def get_action_type_time_trends(events=None, period="Weekly"):
    """Time-series for Action Types view across periods. Scales by filter ratio."""
    if period == "Weekly":
        labels = [f"Week {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "Investigation":   [12, 15, 18, 14, 20, 16, 22, 18, 15, 19],
            "Documentation":   [9, 12, 10, 14, 11, 13, 10, 15, 12, 11],
            "Education":       [6, 8, 5, 9, 7, 8, 6, 10, 8, 7],
            "Escalation":      [5, 7, 8, 6, 9, 7, 8, 6, 7, 8],
            "Policy Update":   [4, 5, 6, 4, 7, 5, 6, 4, 5, 6],
            "System Change":   [3, 4, 3, 5, 4, 3, 5, 3, 4, 4],
        }
    elif period == "Monthly":
        labels = [f"Month {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "Investigation":   [48, 60, 72, 56, 80, 64, 88, 72, 60, 76],
            "Documentation":   [36, 48, 40, 56, 44, 52, 40, 60, 48, 44],
            "Education":       [24, 32, 20, 36, 28, 32, 24, 40, 32, 28],
            "Escalation":      [20, 28, 32, 24, 36, 28, 32, 24, 28, 32],
            "Policy Update":   [16, 20, 24, 16, 28, 20, 24, 16, 20, 24],
            "System Change":   [12, 16, 12, 20, 16, 12, 20, 12, 16, 16],
        }
    else:  # Quarterly
        labels = [f"Q{i}" for i in range(1, 7)]
        data = {
            "Period": labels,
            "Investigation":   [196, 232, 260, 248, 228, 268],
            "Documentation":   [148, 172, 156, 180, 168, 160],
            "Education":       [100, 116, 104, 124, 112, 108],
            "Escalation":      [88, 100, 112, 96, 108, 104],
            "Policy Update":   [68, 80, 88, 72, 84, 80],
            "System Change":   [52, 60, 56, 64, 56, 60],
        }
    if events is not None:
        ratio = len(events) / 6
        for key in ["Investigation", "Documentation", "Education", "Escalation", "Policy Update", "System Change"]:
            data[key] = [max(0, int(v * ratio)) for v in data[key]]
    return pd.DataFrame(data)


def get_severity_time_trends(events=None, period="Weekly"):
    """Time-series for severity breakdown across periods. Scales by filter ratio."""
    if period == "Weekly":
        labels = [f"Week {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "High":   [8, 10, 12, 9, 14, 11, 13, 10, 11, 12],
            "Medium": [18, 22, 20, 25, 21, 24, 19, 23, 22, 20],
            "Low":    [15, 12, 18, 14, 16, 13, 17, 15, 14, 16],
        }
    elif period == "Monthly":
        labels = [f"Month {i}" for i in range(1, 11)]
        data = {
            "Period": labels,
            "High":   [32, 40, 48, 36, 56, 44, 52, 40, 44, 48],
            "Medium": [72, 88, 80, 100, 84, 96, 76, 92, 88, 80],
            "Low":    [60, 48, 72, 56, 64, 52, 68, 60, 56, 64],
        }
    else:  # Quarterly
        labels = [f"Q{i}" for i in range(1, 7)]
        data = {
            "Period": labels,
            "High":   [120, 144, 132, 156, 140, 148],
            "Medium": [248, 272, 260, 288, 268, 276],
            "Low":    [196, 180, 212, 192, 204, 196],
        }
    if events is not None:
        ratio = len(events) / 6
        for key in ["High", "Medium", "Low"]:
            data[key] = [max(0, int(v * ratio)) for v in data[key]]
    return pd.DataFrame(data)


def get_workflow_summary(followups=None):
    """V_WORKFLOW_SUMMARY mock — computes from filtered followups when provided"""
    if followups is None:
        return {
            "closed_with_gaps": 8,
            "review_needed": 33,
            "complete": 0,
            "total_analyzed": 41,
        }
    closed_gaps = sum(1 for f in followups if "Gap" in f.get("status", ""))
    review = sum(1 for f in followups if "Review" in f.get("status", ""))
    total = len(followups)
    return {
        "closed_with_gaps": closed_gaps,
        "review_needed": review,
        "complete": max(0, total - closed_gaps - review),
        "total_analyzed": total,
    }


def get_incomplete_followups():
    """V_INCOMPLETE_FOLLOWUPS mock"""
    return [
        {"file_id": "54115", "status": "Closed w/ Gaps", "pending": 1, "unanswered": 0,
         "urgency": "HIGH", "urgency_count": 3,
         "date_obj": datetime.date(2025, 12, 25), "event_type": "IV/Vascular Access",
         "items": [
             {"level": "HIGH", "desc": "Root cause never determined"},
             {"level": "HIGH", "desc": "\"Will monitor\" – no results documented"},
             {"level": "MED", "desc": "Mitigation plan not documented"},
         ]},
        {"file_id": "53953", "status": "Closed w/ Gaps", "pending": 1, "unanswered": 2,
         "urgency": "HIGH", "urgency_count": 2,
         "date_obj": datetime.date(2025, 12, 20), "event_type": "Medication Error",
         "items": [
             {"level": "HIGH", "desc": "Follow-up investigation not initiated"},
             {"level": "HIGH", "desc": "Policy review pending > 30 days"},
         ]},
        {"file_id": "53810", "status": "Review Needed", "pending": 2, "unanswered": 1,
         "urgency": "MED", "urgency_count": 1,
         "date_obj": datetime.date(2025, 12, 16), "event_type": "Fall",
         "items": [
             {"level": "MED", "desc": "Staff retraining not scheduled"},
         ]},
        {"file_id": "53776", "status": "Review Needed", "pending": 1, "unanswered": 0,
         "urgency": "MED", "urgency_count": 1,
         "date_obj": datetime.date(2025, 12, 14), "event_type": "Skin Integrity",
         "items": [
             {"level": "MED", "desc": "Equipment inspection overdue"},
         ]},
        {"file_id": "54001", "status": "Closed w/ Gaps", "pending": 0, "unanswered": 1,
         "urgency": "HIGH", "urgency_count": 2,
         "date_obj": datetime.date(2025, 12, 22), "event_type": "Nutrition/Feeding",
         "items": [
             {"level": "HIGH", "desc": "No corrective action plan filed"},
             {"level": "MED", "desc": "Incident debrief not documented"},
         ]},
    ]


def get_taxonomy_primary_categories():
    """V_TAXONOMY_REFERENCE WHERE TAXONOMY_TYPE='PROBLEM' AND LEVEL='PRIMARY' mock"""
    return [
        {"name": "Nutrition / Feeding",
         "usage_pct": 28,
         "description": "Events related to dietary orders, meal delivery, NPO status, or feeding tube management.",
         "examples": "Wrong diet delivered, NPO violation, feeding tube displacement, allergy not flagged on tray.",
         "color": "#2196F3"},
        {"name": "IV / Vascular Access",
         "usage_pct": 22,
         "description": "Events involving peripheral or central line insertion, maintenance, infiltration, or removal.",
         "examples": "Infiltration/extravasation, CLABSI, dislodged PICC, line not labeled.",
         "color": "#FF9800"},
        {"name": "Medication Error",
         "usage_pct": 19,
         "description": "Events where a medication was ordered, dispensed, or administered incorrectly.",
         "examples": "Wrong dose, omitted dose, wrong patient, wrong route, look-alike/sound-alike mix-up.",
         "color": "#9C27B0"},
        {"name": "Fall",
         "usage_pct": 12,
         "description": "Unplanned descent to the floor with or without injury, including assisted falls.",
         "examples": "Unassisted fall in bathroom, bed exit alarm failure, fall during transfer.",
         "color": "#009688"},
        {"name": "Skin Integrity",
         "usage_pct": 10,
         "description": "Pressure injuries, skin tears, moisture-associated skin damage, or wound care issues.",
         "examples": "Hospital-acquired pressure injury, skin tear during repositioning, wound dehiscence.",
         "color": "#F44336"},
        {"name": "Documentation Gap",
         "usage_pct": 9,
         "description": "Missing, incomplete, or inaccurate clinical documentation that may affect care continuity.",
         "examples": "Missing consent, incomplete handoff note, allergy not documented, unsigned verbal order.",
         "color": "#FF5722"},
    ]


def get_taxonomy_root_causes():
    """V_TAXONOMY_REFERENCE WHERE TAXONOMY_TYPE='PROBLEM' AND LEVEL='SECONDARY' mock"""
    return [
        {"cause": "System Gap", "description": "Failure in a process, protocol, or system design that allowed the event.",
         "usage_pct": 34, "color": "#F44336"},
        {"cause": "Process Deviation", "description": "Staff did not follow an established procedure or protocol.",
         "usage_pct": 22, "color": "#2196F3"},
        {"cause": "Communication Failure", "description": "Breakdown in verbal, written, or electronic information exchange.",
         "usage_pct": 18, "color": "#9C27B0"},
        {"cause": "Equipment Issue", "description": "Device malfunction, unavailability, or misuse contributing to the event.",
         "usage_pct": 11, "color": "#FF9800"},
        {"cause": "Handoff Failure", "description": "Critical information lost during care transitions between providers or units.",
         "usage_pct": 9, "color": "#FFC107"},
        {"cause": "Human Error", "description": "Unintentional mistake by a trained individual performing a routine task.",
         "usage_pct": 6, "color": "#FF5722"},
    ]


def get_taxonomy_actions():
    """V_TAXONOMY_REFERENCE WHERE TAXONOMY_TYPE='ACTION' mock"""
    return [
        {"category": "Investigation", "description": "Root cause analysis, event review, or fact-finding initiated.",
         "usage_pct": 30, "color": "#1E88E5"},
        {"category": "Staff Education", "description": "Targeted training, simulation, or competency reassessment.",
         "usage_pct": 22, "color": "#009688"},
        {"category": "Process Change", "description": "Workflow, protocol, or policy modification to prevent recurrence.",
         "usage_pct": 18, "color": "#43A047"},
        {"category": "Escalation", "description": "Event elevated to leadership, risk management, or regulatory body.",
         "usage_pct": 14, "color": "#FF9800"},
        {"category": "Equipment Review", "description": "Device inspection, replacement, or vendor notification.",
         "usage_pct": 10, "color": "#9C27B0"},
        {"category": "Documentation Fix", "description": "Chart correction, addendum, or template update.",
         "usage_pct": 6, "color": "#F44336"},
    ]


def get_taxonomy_event_specific_actions():
    """Event-specific action mappings mock"""
    return {
        "Nutrition / Feeding": [
            "Diet Order Change", "Kitchen Coordination", "NPO Protocol Review", "Dietitian Consult"
        ],
        "IV / Vascular Access": [
            "Line Management", "VAT Consultation", "Extravasation Protocol", "Dressing Change Audit"
        ],
        "Medication Error": [
            "Pharmacy Review", "Double-Check Protocol", "High-Alert Med Audit", "BCMA Compliance"
        ],
        "Fall": [
            "Fall Risk Reassessment", "Environment Modification", "1:1 Sitter Evaluation", "Mobility Aid Review"
        ],
    }


def get_taxonomy_cross_cutting():
    """V_CATEGORY_MONITORING WHERE COVERAGE_STATUS LIKE '%CROSS%' mock"""
    return [
        {"pattern": "Process + System Gap", "nutrition": 12, "iv_vascular": 9, "medication": 7, "total": 28},
        {"pattern": "Communication + Handoff", "nutrition": 6, "iv_vascular": 8, "medication": 5, "total": 19},
        {"pattern": "Documentation + Process", "nutrition": 5, "iv_vascular": 4, "medication": 6, "total": 15},
        {"pattern": "Equipment + System Gap", "nutrition": 2, "iv_vascular": 7, "medication": 3, "total": 12},
        {"pattern": "Human Error + Communication", "nutrition": 4, "iv_vascular": 3, "medication": 4, "total": 11},
    ]


def get_datix_crosswalk():
    """V_DATIX_CROSSWALK mock — dynamically derived from event + taxonomy data."""
    events = get_event_list()
    clinical = get_clinical_category_summary()  # secondaries keyed by event_type
    cat_names = {c["name"] for c in get_taxonomy_primary_categories()}

    def _resolve_primary(event_type):
        if event_type in cat_names:
            return event_type
        spaced = event_type.replace("/", " / ")
        if spaced in cat_names:
            return spaced
        return event_type

    # Collect distinct datix → new-taxonomy mappings, grouped by primary
    groups = {}  # new_event_type → {primary, secondaries, mappings[]}
    for e in events:
        et = e["event_type"]
        if et not in groups:
            secs = [c["category"] for c in clinical.get(et, {}).get("categories", [])]
            groups[et] = {
                "new_event_type": et,
                "new_primary_category": _resolve_primary(et),
                "secondaries": secs,
                "mappings": [],
                "_seen": set(),
            }
        key = (e["datix_general"], e["datix_specific"])
        if key not in groups[et]["_seen"]:
            groups[et]["_seen"].add(key)
            groups[et]["mappings"].append({
                "datix_general": e["datix_general"],
                "datix_specific": e["datix_specific"],
            })

    # Sort groups by primary name, mappings within each group alphabetically
    result = []
    for g in sorted(groups.values(), key=lambda g: g["new_primary_category"]):
        g["mappings"].sort(key=lambda m: (m["datix_general"], m["datix_specific"]))
        result.append({
            "new_event_type": g["new_event_type"],
            "new_primary_category": g["new_primary_category"],
            "secondaries": g["secondaries"],
            "mappings": g["mappings"],
        })
    return result


def get_unit_locations():
    """Extract distinct location values from event list, sorted."""
    events = get_event_list()
    return sorted(set(e["location"] for e in events))


def get_liaison_mapping():
    """SAFETY_LIAISON_MAPPING mock"""
    return [
        {"liaison_name": "TBD - Liaison A", "territory_name": "Critical Care North",
         "assigned_locations": ["22nd Floor", "21st Floor", "20th Floor"],
         "specialty_event_types": ["IV/Vascular Access"], "is_hospital_wide": False},
        {"liaison_name": "TBD - Liaison B", "territory_name": "Critical Care South",
         "assigned_locations": ["17th Floor", "16th Floor", "18th Floor"],
         "specialty_event_types": ["IV/Vascular Access"], "is_hospital_wide": False},
        {"liaison_name": "TBD - Liaison C", "territory_name": "Med-Surg East",
         "assigned_locations": ["14th Floor", "15th N Floor", "15th S Floor"],
         "specialty_event_types": ["IV/Vascular Access", "Nutrition/Feeding"], "is_hospital_wide": False},
        {"liaison_name": "TBD - Liaison D", "territory_name": "Med-Surg West",
         "assigned_locations": ["19th Floor", "6th Floor", "5th Floor"],
         "specialty_event_types": ["Nutrition/Feeding"], "is_hospital_wide": False},
        {"liaison_name": "TBD - Liaison E", "territory_name": "Procedural Areas",
         "assigned_locations": ["2nd Floor", "3rd Floor", "4th Floor", "1st Floor"],
         "specialty_event_types": [], "is_hospital_wide": False},
        {"liaison_name": "TBD - Liaison F", "territory_name": "Specialty Units",
         "assigned_locations": ["7th Floor", "8th Floor", "9th Floor"],
         "specialty_event_types": [], "is_hospital_wide": False},
        {"liaison_name": "TBD - VAT Lead", "territory_name": "Hospital-Wide IV",
         "assigned_locations": [], "specialty_event_types": ["IV/Vascular Access"], "is_hospital_wide": True},
        {"liaison_name": "TBD - Nutrition Lead", "territory_name": "Hospital-Wide Nutrition",
         "assigned_locations": [], "specialty_event_types": ["Nutrition/Feeding"], "is_hospital_wide": True},
    ]

def get_liaison_by_name(name):
    """Look up a single liaison record by name."""
    for m in get_liaison_mapping():
        if m["liaison_name"] == name:
            return m
    return None


def filter_events_by_unit(events, unit):
    """Filter event list to a single location. Returns full list if unit is falsy."""
    if not unit:
        return events
    return [e for e in events if e.get("location") == unit]


def filter_events_by_territory(events, liaison, selected_floor=None):
    """Filter events for a liaison's territory, with optional floor drill-down."""
    if not liaison:
        return events
    # 1. Location scope
    if liaison["is_hospital_wide"]:
        result = events
    else:
        assigned = set(liaison["assigned_locations"])
        result = [e for e in events if e.get("location") in assigned]
    # 2. Hospital-wide specialty filter
    if liaison["is_hospital_wide"] and liaison["specialty_event_types"]:
        spec = set(liaison["specialty_event_types"])
        result = [e for e in result if e.get("event_type") in spec]
    # 3. Floor drill-down
    if selected_floor and selected_floor != "All Floors":
        result = [e for e in result if e.get("location") == selected_floor]
    return result


def get_liaison_context():
    """Resolve current liaison selection into a context dict for page rendering."""
    name = st.session_state.get("liaison_name", "")
    liaison = get_liaison_by_name(name)
    floor = st.session_state.get("liaison_floor", "All Floors")
    if not liaison:
        return {"liaison": None, "territory_name": "", "selected_floor": None, "header_suffix": ""}
    territory = liaison["territory_name"]
    if floor and floor != "All Floors":
        header = f"{territory} \u203a {floor}"
    else:
        header = territory
    return {
        "liaison": liaison,
        "territory_name": territory,
        "selected_floor": floor if floor != "All Floors" else None,
        "header_suffix": header,
    }


def compute_completeness_score(event):
    """Compare suggested_actions vs actual_followups using keyword overlap.
    Returns (matched, total, pct)."""
    suggested = event.get("suggested_actions", [])
    followups = event.get("actual_followups", [])
    if not suggested:
        return (0, 0, 100)
    followup_words = set()
    for f in followups:
        for w in f.get("action", "").lower().split():
            followup_words.add(w)
    matched = 0
    for s in suggested:
        s_words = set(s.lower().split())
        if len(s_words & followup_words) >= 2:
            matched += 1
    total = len(suggested)
    pct = int(round(matched / total * 100)) if total > 0 else 100
    return (matched, total, pct)


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    _logo_path = Path(__file__).parent / "lurie_logo.png"
    st.image(str(_logo_path), width=160)
    st.html("""<div class="sidebar-logo">
        <div class="sidebar-logo-title">Safety Intelligence</div>
        <div class="sidebar-logo-sub">AI-Powered Event Analysis</div>
    </div>""")

    user_role = st.selectbox("Role", ["Central Safety Team", "Department Liaison"], key="user_role")

    if user_role == "Central Safety Team":
        page = st.radio(
            "Navigation",
            ["Dashboard", "Event Explorer", "Routing Intelligence",
             "Trend Analysis", "Workflow Monitor", "Taxonomy Reference"],
            label_visibility="collapsed",
        )
    else:
        page = st.radio(
            "Navigation",
            ["My Events", "Follow-Up Workspace", "Department Trends", "Taxonomy Reference"],
            label_visibility="collapsed",
            key="liaison_nav",
        )
        # Liaison selector
        mapping = get_liaison_mapping()
        liaison_names = [m["liaison_name"] for m in mapping]
        st.selectbox("My Name", liaison_names, key="liaison_name")

        selected_liaison = get_liaison_by_name(
            st.session_state.get("liaison_name", liaison_names[0])
        )

        if selected_liaison:
            st.html(
                f'<div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;'
                f'letter-spacing:0.05em;color:#94a3b8;margin-top:2px;">TERRITORY</div>'
                f'<div style="font-size:0.85rem;color:#cbd5e1;margin-bottom:4px;">'
                f'{selected_liaison["territory_name"]}</div>'
            )

            # Reset floor when liaison changes
            current = st.session_state.get("liaison_name", "")
            if current != st.session_state.get("_prev_liaison", ""):
                st.session_state["liaison_floor"] = "All Floors"
                st.session_state["_prev_liaison"] = current

            # Floor drill-down
            if selected_liaison["is_hospital_wide"]:
                floor_options = ["All Floors"] + get_unit_locations()
            else:
                floor_options = ["All Floors"] + selected_liaison["assigned_locations"]
            st.selectbox("Floor", floor_options, key="liaison_floor")

    st.divider()

    date_range = st.date_input(
        "Date Range",
        value=(datetime.date(2025, 12, 1), datetime.date(2025, 12, 31)),
        key="global_date_range",
    )
    st.selectbox("Event Type Filter", ["All Types", "Nutrition/Feeding", "IV/Vascular Access",
                                        "Medication Error", "Fall", "Skin Integrity"], key="event_type_filter")
    st.selectbox("Severity Filter", ["All Severities", "High", "Medium", "Low"], key="severity_filter")
    if user_role == "Central Safety Team":
        st.selectbox("Location Filter", ["All Locations", "2nd Floor", "7th Floor", "16th Floor", "17th Floor", "18th Floor"], key="location_filter")
    st.selectbox("Datix Category (EVENT_TYPE)", ["All Datix Categories", "Nutrition/Diet", "Equipment/Medical Device", "Medication", "Patient Accident", "Clinical Treatment"], key="datix_general_filter")
    st.selectbox("Datix Specific (SPECIFIC_EVENT_TYPE_REPORTED)", ["All Datix Specific", "NPO Violation", "Line Infection", "Wrong Dose", "Fall", "Pressure Injury", "Dislodgement"], key="datix_specific_filter")

    st.divider()
    st.html('<div class="sidebar-version"><span class="dot"></span> v0.2 &mdash; Mock Data</div>')


# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL FILTER HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def get_global_filters():
    """Read sidebar filter state, handling edge cases."""
    raw_date = st.session_state.get("global_date_range", (datetime.date(2025, 12, 1), datetime.date(2025, 12, 31)))
    if isinstance(raw_date, (list, tuple)):
        if len(raw_date) == 2:
            start_date, end_date = raw_date
        elif len(raw_date) == 1:
            start_date = raw_date[0]
            end_date = datetime.date(2025, 12, 31)
        else:
            start_date, end_date = datetime.date(2025, 12, 1), datetime.date(2025, 12, 31)
    else:
        start_date = raw_date
        end_date = datetime.date(2025, 12, 31)
    event_type = st.session_state.get("event_type_filter", "All Types")
    severity = st.session_state.get("severity_filter", "All Severities")
    location = st.session_state.get("location_filter", "All Locations")
    datix_general = st.session_state.get("datix_general_filter", "All Datix Categories")
    datix_specific = st.session_state.get("datix_specific_filter", "All Datix Specific")
    return {"start_date": start_date, "end_date": end_date, "event_type": event_type, "severity": severity, "location": location, "datix_general": datix_general, "datix_specific": datix_specific}


def apply_global_filters(items, filters):
    """Filter a list of dicts by date range and event type using date_obj and event_type fields."""
    result = items
    start, end = filters["start_date"], filters["end_date"]
    result = [i for i in result if i.get("date_obj") is None or start <= i["date_obj"] <= end]
    if filters["event_type"] != "All Types":
        result = [i for i in result if i.get("event_type") == filters["event_type"]]
    if filters["severity"] != "All Severities":
        result = [i for i in result if i.get("severity") == filters["severity"]]
    if filters["location"] != "All Locations":
        result = [i for i in result if i.get("location") == filters["location"]]
    if filters["datix_general"] != "All Datix Categories":
        result = [i for i in result if i.get("datix_general") == filters["datix_general"]]
    if filters["datix_specific"] != "All Datix Specific":
        result = [i for i in result if i.get("datix_specific") == filters["datix_specific"]]
    return result


def apply_event_type_filter_multi(items, filters):
    """Filter items that have an event_types list field (e.g. routing alerts)."""
    if filters["event_type"] == "All Types":
        return items
    return [i for i in items if filters["event_type"] in i.get("event_types", [])]


# Active filter indicator in sidebar
_filters_preview = get_global_filters()
_default_start = datetime.date(2025, 12, 1)
_default_end = datetime.date(2025, 12, 31)
_is_date_filtered = (_filters_preview["start_date"] != _default_start or _filters_preview["end_date"] != _default_end)
_is_type_filtered = _filters_preview["event_type"] != "All Types"
_is_sev_filtered = _filters_preview["severity"] != "All Severities"
_is_loc_filtered = _filters_preview["location"] != "All Locations"
_is_datix_gen_filtered = _filters_preview["datix_general"] != "All Datix Categories"
_is_datix_spec_filtered = _filters_preview["datix_specific"] != "All Datix Specific"
if _is_date_filtered or _is_type_filtered or _is_sev_filtered or _is_loc_filtered or _is_datix_gen_filtered or _is_datix_spec_filtered:
    _parts = []
    if _is_date_filtered:
        _parts.append(f'{_filters_preview["start_date"].strftime("%b %d")} – {_filters_preview["end_date"].strftime("%b %d")}')
    if _is_type_filtered:
        _parts.append(_filters_preview["event_type"])
    if _is_sev_filtered:
        _parts.append(_filters_preview["severity"])
    if _is_loc_filtered:
        _parts.append(_filters_preview["location"])
    if _is_datix_gen_filtered:
        _parts.append(f'Datix: {_filters_preview["datix_general"]}')
    if _is_datix_spec_filtered:
        _parts.append(f'Datix: {_filters_preview["datix_specific"]}')
    with st.sidebar:
        st.html(f'<div style="background:rgba(30,136,229,0.15);border:1px solid rgba(30,136,229,0.3);border-radius:8px;padding:6px 12px;font-size:0.78rem;color:#93c5fd;margin-top:4px;">Active filters: {" | ".join(_parts)}</div>')


# ──────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────
def render_kpi(value, label, color_class="primary", border_class="kpi-border-blue"):
    return f"""
    <div class="kpi-card {border_class}">
        <div class="kpi-value {color_class}">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """

def render_kpi_with_delta(value, label, delta, delta_label, color_class="primary", border_class="kpi-border-blue"):
    arrow = "&#9650;" if delta >= 0 else "&#9660;"
    delta_color = "#E53935" if delta > 0 else "#43A047" if delta < 0 else "#64748b"
    sign = "+" if delta > 0 else ""
    return f"""
    <div class="kpi-card {border_class}">
        <div class="kpi-value {color_class}">{value}</div>
        <div class="kpi-label">{label}</div>
        <div style="font-size:0.78rem;color:{delta_color};font-weight:600;margin-top:4px;">
            {arrow} {sign}{delta}% {delta_label}
        </div>
    </div>
    """


def compute_trend_analysis_summary(trends_df, root_causes, action_trends):
    """Dynamically compute 4 summary values from actual data."""
    # Most Common Root Cause
    if root_causes:
        top_rc = max(root_causes, key=lambda x: x["pct"])
        most_common = f'{top_rc["cause"]} ({top_rc["pct"]}%)'
    else:
        most_common = "N/A"

    # Fastest Growing — largest last-vs-prior increase in trends_df
    numeric_cols = [c for c in trends_df.columns if c != "Period"]
    fastest_name, fastest_pct = "N/A", 0
    improving_name, improving_pct = "N/A", 0
    if len(trends_df) >= 2:
        for col in numeric_cols:
            last = trends_df[col].iloc[-1]
            prior = trends_df[col].iloc[-2]
            if prior > 0:
                change = int(round((last - prior) / prior * 100))
            else:
                change = 0
            if change > fastest_pct:
                fastest_pct = change
                fastest_name = col
            if change < improving_pct:
                improving_pct = change
                improving_name = col

    fastest_growing = f'{fastest_name} (+{fastest_pct}%)' if fastest_name != "N/A" else "N/A"
    improving_area = f'{improving_name} ({improving_pct}%)' if improving_name != "N/A" else "N/A"

    # Top Action Type
    if action_trends:
        top_at = max(action_trends, key=lambda x: x["pct"])
        top_action = f'{top_at["action_type"]} ({top_at["pct"]}%)'
    else:
        top_action = "N/A"

    return {
        "most_common": most_common,
        "fastest_growing": fastest_growing,
        "top_action": top_action,
        "improving_area": improving_area,
    }


def render_severity_badge(level):
    level_lower = level.lower()
    if level_lower in ("high", "immediate", "urgent"):
        return f'<span class="sev-high">{level}</span>'
    elif level_lower in ("medium", "med"):
        return f'<span class="sev-med">{level}</span>'
    else:
        return f'<span class="sev-low">{level}</span>'

def render_bar(label, pct, color="bar-blue"):
    return f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
        <div style="width:140px;font-size:0.85rem;color:#334155;font-weight:500;">{label}</div>
        <div class="bar-container" style="flex:1;">
            <div class="bar-fill {color}" style="width:{pct}%;">{pct}%</div>
        </div>
    </div>
    """

def urgency_html(level):
    cls_map = {"IMMEDIATE": "urgency-imm", "URGENT": "urgency-urg", "HIGH": "urgency-high", "MEDIUM": "urgency-med", "MED": "urgency-med", "LOW": "urgency-med"}
    cls = cls_map.get(level, "urgency-med")
    return f'<span class="{cls}">{level}</span>'


def render_completeness_score(matched, total, pct):
    """Render the score-ring HTML with matched/total count and contextual color."""
    if pct >= 75:
        ring_cls = "score-high"
    elif pct >= 40:
        ring_cls = "score-med"
    else:
        ring_cls = "score-low"
    return f"""
    <div style="text-align:center;">
        <div class="score-ring {ring_cls}" style="--pct:{pct};">{pct}%</div>
        <div style="font-size:0.82rem;font-weight:600;color:#334155;">{matched} of {total} actions addressed</div>
    </div>
    """


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":
    st.markdown("## Executive Dashboard")

    filters = get_global_filters()
    all_events = get_event_list()
    filtered_events = apply_global_filters(all_events, filters)
    filtered_escalations = apply_global_filters(get_escalation_queue(), filters)
    digest = get_weekly_digest(filtered_events, filtered_escalations)

    if not filtered_events and not filtered_escalations:
        st.info("No events match the current filters.")

    # KPI Row
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.html(render_kpi(digest["events_analyzed"], "Events Analyzed", "primary", "kpi-border-blue"))
    with k2:
        st.html(render_kpi(digest["problems_found"], "Problems Found", "primary", "kpi-border-purple"))
    with k3:
        st.html(render_kpi(digest["high_severity"], "High Severity", "warn", "kpi-border-orange"))
    with k4:
        st.html(render_kpi(digest["urgent_escalations"], "Urgent Escalations", "urgent", "kpi-border-red"))
    with k5:
        st.html(render_kpi(digest["routing_alerts"], "Routing Alerts", "warn", "kpi-border-orange"))

    st.html("<div style='height:0.75rem'></div>")

    # Two-column: Categories + Location Risk
    col_left, col_right = st.columns(2)

    with col_left:
        categories = get_category_summary(filtered_events)
        bars_html = "".join(
            render_bar(c["category"], c["pct"],
                       ["bar-blue", "bar-orange", "bar-teal", "bar-purple", "bar-green", "bar-red"][i % 6])
            for i, c in enumerate(categories)
        )
        st.html(f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">Top Problem Categories</div>
            </div>
            {bars_html}
        </div>
        """)

    with col_right:
        locations = get_location_risk(filtered_events)
        rows_html = ""
        for loc in locations:
            bar_color = {"HIGH": "#E53935", "MEDIUM": "#FB8C00", "LOW": "#43A047"}[loc["level"]]
            heat_bg = {"HIGH": "#fee2e2", "MEDIUM": "#ffedd5", "LOW": "#dcfce7"}[loc["level"]]
            heat_fg = {"HIGH": "#991b1b", "MEDIUM": "#9a3412", "LOW": "#166534"}[loc["level"]]
            bar_w = loc["risk_score"]
            rows_html += f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                <div style="width:180px;font-size:0.85rem;color:#334155;font-weight:500;">{loc["location"]}</div>
                <div style="flex:1;background:#f1f5f9;border-radius:6px;height:22px;overflow:hidden;">
                    <div style="width:{bar_w}%;height:100%;border-radius:6px;display:flex;align-items:center;padding-left:8px;font-size:0.72rem;font-weight:700;color:#fff;background:{bar_color};">{loc["risk_score"]}</div>
                </div>
                <div style="min-width:70px;text-align:center;background:{heat_bg};color:{heat_fg};font-weight:700;padding:8px 16px;border-radius:6px;">{loc["level"]}</div>
            </div>
            """
        st.html(f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">Location Risk Heatmap</div>
            </div>
            {rows_html}
        </div>
        """)

    # Clinical Category Spotlight
    clinical_data = get_clinical_category_summary(filtered_events)
    if clinical_data:
        groups_html = ""
        for et, data in clinical_data.items():
            color = data["color"]
            items_html = ""
            for c in data["categories"][:3]:
                bar_w = min(c["pct"] * 2, 100)
                items_html += f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                    <div style="width:160px;font-size:0.82rem;color:#334155;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="{c['category']}">{c['category']}</div>
                    <div style="font-size:0.78rem;font-weight:700;color:#475569;min-width:24px;text-align:right;">{c['count']}</div>
                    <div style="flex:1;background:#f1f5f9;border-radius:4px;height:6px;overflow:hidden;">
                        <div style="width:{bar_w}%;height:100%;border-radius:4px;background:{color};"></div>
                    </div>
                </div>"""
            groups_html += f"""
            <div style="flex:1;min-width:180px;">
                <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;">
                    <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{color};"></span>
                    <span style="font-size:0.85rem;font-weight:700;color:#1e293b;">{et}</span>
                </div>
                {items_html}
            </div>"""
        st.html(f"""
        <div class="card card-purple">
            <div class="card-header">
                <div class="card-title">Clinical Category Spotlight</div>
                <span class="badge badge-blue">{len(clinical_data)} Event Types</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:24px;padding-top:4px;">
                {groups_html}
            </div>
        </div>
        """)

    # Urgent Escalations
    escalations = filtered_escalations
    esc_rows = ""
    for e in escalations:
        esc_rows += f"""
        <tr>
            <td><strong>{e["file_id"]}</strong></td>
            <td><span class="chip">{e["event_type"]}</span></td>
            <td>{e["location"]}</td>
            <td>{e["date"]}</td>
            <td>{urgency_html(e["urgency"])}</td>
            <td style="font-size:0.82rem;color:#475569;">{e["reason"]}</td>
        </tr>
        """
    st.html(f"""
    <div class="card card-red">
        <div class="card-header">
            <div class="card-title">Urgent Escalations</div>
            <span class="badge badge-red">{len(escalations)} Active</span>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>File ID</th>
                    <th>Event Type</th>
                    <th>Location</th>
                    <th>Date</th>
                    <th>Urgency</th>
                    <th>Reason</th>
                </tr>
            </thead>
            <tbody>{esc_rows}</tbody>
        </table>
    </div>
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: EVENT EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Event Explorer":
    st.markdown("## Event Explorer")

    filters = get_global_filters()
    events = apply_global_filters(get_event_list(), filters)

    if not events:
        st.info("No events match the current global filters.")

    # Filters (local, narrowing from globally-filtered list)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        type_filter = st.selectbox("Event Type", ["All"] + sorted(set(e["event_type"] for e in events)), key="explorer_type")
    with fc2:
        loc_filter = st.selectbox("Location", ["All"] + sorted(set(e["location"] for e in events)), key="explorer_loc")
    with fc3:
        sev_filter = st.selectbox("Severity", ["All", "High", "Medium", "Low"], key="explorer_sev")

    # Apply local filters
    filtered = events
    if type_filter != "All":
        filtered = [e for e in filtered if e["event_type"] == type_filter]
    if loc_filter != "All":
        filtered = [e for e in filtered if e["location"] == loc_filter]
    if sev_filter != "All":
        filtered = [e for e in filtered if e["severity"] == sev_filter]

    # Event table
    evt_rows = ""
    for e in filtered:
        sev_badge = render_severity_badge(e["severity"])
        status_cls = "badge-orange" if "Review" in e["status"] else "badge-red" if "Escalat" in e["status"] else "badge-green"
        evt_rows += f"""
        <tr>
            <td><strong>{e["file_id"]}</strong></td>
            <td><span class="chip">{e["event_type"]}</span><div style="font-size:0.7rem;color:#94a3b8;margin-top:2px;">Datix: {e["datix_general"]} &rsaquo; {e["datix_specific"]}</div></td>
            <td>{e["date"]}</td>
            <td>{e["location"]}</td>
            <td style="text-align:center;font-weight:600;">{e["problems"]}</td>
            <td style="text-align:center;font-weight:600;color:{"#E53935" if e["gaps"]>0 else "#43A047"};">{e["gaps"]}</td>
            <td>{sev_badge}</td>
            <td><span class="badge {status_cls}">{e["status"]}</span></td>
        </tr>
        """

    st.html(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title">Safety Events</div>
            <span class="badge badge-blue">{len(filtered)} events</span>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>File ID</th>
                    <th>Type</th>
                    <th>Date</th>
                    <th>Location</th>
                    <th>Problems</th>
                    <th>Gaps</th>
                    <th>Severity</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{evt_rows}</tbody>
        </table>
    </div>
    """)

    # Detail panel
    if filtered:
        selected_id = st.selectbox(
            "Select event to view details",
            [e["file_id"] for e in filtered],
            key="event_detail_select",
        )
        event = next(e for e in filtered if e["file_id"] == selected_id)

        # Narrative
        st.html(f"""
        <div class="card card-purple">
            <div class="card-header">
                <div class="card-title">Event Detail: {event["file_id"]}</div>
                {render_severity_badge(event["severity"])}
            </div>
            <div style="font-size:0.75rem;color:#94a3b8;margin-bottom:8px;">Datix: {event["datix_general"]} &rsaquo; {event["datix_specific"]}</div>
            <div class="summary-label">NARRATIVE</div>
            <div class="narrative">{event["narrative"]}</div>
        </div>
        """)

        # Problems + Suggested Actions | Actual Follow-ups + Gaps
        p_col, a_col = st.columns(2)

        with p_col:
            problems_html = ""
            for i, p in enumerate(event["problems_detail"], 1):
                problems_html += f"""
                <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;">
                    <div style="min-width:22px;height:22px;border-radius:50%;background:#1E88E5;color:#fff;font-size:0.72rem;font-weight:700;display:flex;align-items:center;justify-content:center;">{i}</div>
                    <div>
                        <div style="font-size:0.88rem;color:#1e293b;">{p["problem"]}</div>
                        <div><span class="chip">{p["category"]}</span></div>
                    </div>
                </div>
                """
            actions_html = ""
            for a in event["suggested_actions"]:
                actions_html += f'<div style="font-size:0.85rem;color:#475569;margin-bottom:4px;"><span class="dot-blue"></span>{a}</div>'

            st.html(f"""
            <div class="card">
                <div class="card-title" style="margin-bottom:0.75rem;">Problems Identified</div>
                {problems_html}
                <div style="margin-top:1rem;">
                    <div class="summary-label" style="margin-bottom:0.5rem;">SUGGESTED ACTIONS</div>
                    {actions_html}
                </div>
            </div>
            """)

        with a_col:
            followups_html = ""
            for f in event["actual_followups"]:
                followups_html += f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <div><span class="badge badge-blue">{f["type"]}</span></div>
                    <div style="font-size:0.88rem;color:#334155;">{f["action"]}</div>
                </div>
                """
            gaps_html = ""
            for g in event["gaps_detail"]:
                gaps_html += f'<div style="font-size:0.85rem;color:#991b1b;margin-bottom:4px;"><span class="dot-red"></span>{g}</div>'
            if not event["gaps_detail"]:
                gaps_html = '<div style="font-size:0.85rem;color:#43A047;"><span class="dot-green"></span>No gaps identified</div>'

            st.html(f"""
            <div class="card card-green">
                <div class="card-title" style="margin-bottom:0.75rem;">Actual Follow-ups</div>
                {followups_html}
                <div style="margin-top:1rem;">
                    <div class="summary-label" style="margin-bottom:0.5rem;">GAPS IDENTIFIED</div>
                    {gaps_html}
                </div>
            </div>
            """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3: ROUTING INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Routing Intelligence":
    st.markdown("## Routing Intelligence")

    filters = get_global_filters()
    alerts = apply_event_type_filter_multi(get_routing_alerts(), filters)
    actions = apply_global_filters(get_routing_action_items(), filters)

    if not alerts and not actions:
        st.info("No routing data matches the current filters.")

    # Routing Alerts by Department
    alert_rows = ""
    for a in alerts:
        lvl_cls = {"HIGH": "sev-high", "MEDIUM": "sev-med", "LOW": "sev-low"}[a["level"]]
        alert_rows += f"""
        <tr>
            <td style="font-weight:600;">{a["department"]}</td>
            <td style="text-align:center;font-weight:700;font-size:1.05rem;">{a["events_missing"]}</td>
            <td><span class="{lvl_cls}">{a["level"]}</span></td>
            <td style="font-size:0.82rem;color:#475569;">{a["description"]}</td>
        </tr>
        """

    st.html(f"""
    <div class="card card-red">
        <div class="card-header">
            <div class="card-title">Routing Alerts by Department</div>
            <span class="badge badge-red">{sum(a["events_missing"] for a in alerts)} Total Missing</span>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Department</th>
                    <th style="text-align:center;">Events Missing</th>
                    <th>Alert Level</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>{alert_rows}</tbody>
        </table>
    </div>
    """)

    # Events Needing Routing Correction
    action_rows = ""
    for a in actions:
        pri_cls = {"URGENT": "sev-high", "HIGH": "sev-med", "MEDIUM": "sev-low"}[a["priority"]]
        tags = " ".join(f'<span class="chip">{t.strip()}</span>' for t in a["must_tag"].split(","))
        action_rows += f"""
        <tr>
            <td><strong>{a["file_id"]}</strong></td>
            <td>{a["reported_to"]}</td>
            <td style="font-weight:600;color:#1E88E5;">{a["should_be"]}</td>
            <td>{tags}</td>
            <td><span class="{pri_cls}">{a["priority"]}</span></td>
        </tr>
        """

    st.html(f"""
    <div class="card card-orange">
        <div class="card-header">
            <div class="card-title">Events Needing Routing Correction</div>
            <span class="badge badge-orange">{len(actions)} Items</span>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>File ID</th>
                    <th>Reported To</th>
                    <th>Should Be</th>
                    <th>Must Tag</th>
                    <th>Priority</th>
                </tr>
            </thead>
            <tbody>{action_rows}</tbody>
        </table>
    </div>
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: TREND ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Trend Analysis":
    st.markdown("## Trend Analysis")

    filters = get_global_filters()
    filtered_events = apply_global_filters(get_event_list(), filters)

    if not filtered_events:
        st.info("No events match the current filters.")

    # ── Controls ──────────────────────────────────────────────────────────
    fc1, fc2 = st.columns(2)
    with fc1:
        view_option = st.selectbox("View", ["Event Types", "Clinical Subcategories", "Root Causes", "Action Types"], key="trend_view")
    with fc2:
        period_option = st.selectbox("Period", ["Weekly", "Monthly", "Quarterly"], key="trend_period")

    if view_option == "Clinical Subcategories":
        topn_option = st.selectbox("Show", ["Top 5", "Top 10", "All"], index=1, key="trend_topn")
    else:
        topn_option = "All"

    # ── Fetch data based on View selection ────────────────────────────────
    if view_option == "Event Types":
        trends_df = get_event_type_time_trends(filtered_events, period=period_option)
        chart_title = "Event Type Trends"
    elif view_option == "Clinical Subcategories":
        trends_df = get_clinical_subcategory_time_trends(filtered_events, period=period_option)
        chart_title = "Clinical Subcategory Trends"
    elif view_option == "Root Causes":
        trends_df = get_root_cause_time_trends(filtered_events, period=period_option)
        chart_title = "Root Cause Trends"
    else:  # Action Types
        trends_df = get_action_type_time_trends(filtered_events, period=period_option)
        chart_title = "Action Type Trends"

    kpi_total_label = {
        "Event Types": "Total Events",
        "Clinical Subcategories": "Total Subcategory Events",
        "Root Causes": "Total Root Causes",
        "Action Types": "Total Actions",
    }[view_option]

    if view_option == "Clinical Subcategories" and topn_option != "All":
        n = int(topn_option.split()[1])
        numeric_cols_all = [c for c in trends_df.columns if c != "Period"]
        last_vals = {c: trends_df[c].iloc[-1] for c in numeric_cols_all}
        top_cols = sorted(last_vals, key=last_vals.get, reverse=True)[:n]
        trends_df = trends_df[["Period"] + top_cols]

    severity_df = get_severity_time_trends(filtered_events, period=period_option)
    root_causes = get_root_cause_distribution(filtered_events)
    action_trends = get_action_trends(filtered_events)

    # ── KPIs ──────────────────────────────────────────────────────────────
    numeric_cols = [c for c in trends_df.columns if c != "Period"]
    total_last = int(trends_df[numeric_cols].iloc[-1].sum()) if len(trends_df) > 0 else 0
    total_prior = int(trends_df[numeric_cols].iloc[-2].sum()) if len(trends_df) >= 2 else total_last
    period_change = int(round((total_last - total_prior) / total_prior * 100)) if total_prior > 0 else 0

    highest_cat = ""
    highest_val = 0
    trending_cat = ""
    trending_change = 0
    if len(trends_df) >= 2:
        for col in numeric_cols:
            if trends_df[col].iloc[-1] > highest_val:
                highest_val = int(trends_df[col].iloc[-1])
                highest_cat = col
            last_v = trends_df[col].iloc[-1]
            prior_v = trends_df[col].iloc[-2]
            ch = int(round((last_v - prior_v) / prior_v * 100)) if prior_v > 0 else 0
            if ch > trending_change:
                trending_change = ch
                trending_cat = col

    kc1, kc2, kc3, kc4 = st.columns(4)
    with kc1:
        st.html(render_kpi_with_delta(total_last, kpi_total_label, period_change, "vs prior", color_class="primary", border_class="kpi-border-blue"))
    with kc2:
        change_color = "accent" if period_change > 0 else "primary"
        change_border = "kpi-border-red" if period_change > 0 else "kpi-border-green"
        st.html(render_kpi_with_delta(f"{period_change:+d}%", "Period Change", period_change, "trend", color_class=change_color, border_class=change_border))
    with kc3:
        st.html(render_kpi(f"{highest_cat}", f"Highest ({highest_val})", color_class="primary", border_class="kpi-border-purple"))
    with kc4:
        st.html(render_kpi(f"{trending_cat}", f"Trending (+{trending_change}%)", color_class="accent", border_class="kpi-border-orange"))

    # ── Main Stacked Area Chart ───────────────────────────────────────────
    st.html(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title">{chart_title}</div>
        </div>
    </div>
    """)
    st.area_chart(trends_df.set_index("Period"), use_container_width=True)

    st.html("<div style='height:0.5rem'></div>")

    # ── View-aware panel data ──────────────────────────────────────────────
    if view_option == "Event Types":
        tax_cats = get_taxonomy_primary_categories()
        left_title = "Event Type Distribution"
        left_items = [{"label": c["name"], "pct": c["usage_pct"]} for c in tax_cats]
        right_dist_title = "Root Cause Distribution"
        right_dist_items = [{"label": rc["cause"], "pct": rc["pct"]} for rc in root_causes]
        most_common_label = "Most Common Event Type"
        top_left = max(left_items, key=lambda x: x["pct"]) if left_items else None
        most_common_value = f'{top_left["label"]} ({top_left["pct"]}%)' if top_left else "N/A"
    elif view_option == "Clinical Subcategories":
        ccs = get_clinical_category_summary(filtered_events)
        flat = []
        for _parent, data in ccs.items():
            for c in data["categories"]:
                flat.append({"label": c["category"], "count": c["count"]})
        total_count = sum(item["count"] for item in flat) or 1
        left_items = [{"label": item["label"], "pct": int(round(item["count"] / total_count * 100))}
                      for item in sorted(flat, key=lambda x: x["count"], reverse=True)]
        left_title = "Subcategory Distribution"
        right_dist_title = "Root Cause Distribution"
        right_dist_items = [{"label": rc["cause"], "pct": rc["pct"]} for rc in root_causes]
        most_common_label = "Most Common Subcategory"
        top_left = left_items[0] if left_items else None
        most_common_value = f'{top_left["label"]} ({top_left["pct"]}%)' if top_left else "N/A"
    elif view_option == "Root Causes":
        left_title = "Root Cause Distribution"
        left_items = [{"label": rc["cause"], "pct": rc["pct"]} for rc in root_causes]
        right_dist_title = "Action Type Distribution"
        right_dist_items = [{"label": at["action_type"], "pct": at["pct"]} for at in action_trends]
        most_common_label = "Most Common Root Cause"
        top_left = max(left_items, key=lambda x: x["pct"]) if left_items else None
        most_common_value = f'{top_left["label"]} ({top_left["pct"]}%)' if top_left else "N/A"
    else:  # Action Types
        left_title = "Action Type Distribution"
        left_items = [{"label": at["action_type"], "pct": at["pct"]} for at in action_trends]
        right_dist_title = "Root Cause Distribution"
        right_dist_items = [{"label": rc["cause"], "pct": rc["pct"]} for rc in root_causes]
        most_common_label = "Most Common Action"
        top_left = max(left_items, key=lambda x: x["pct"]) if left_items else None
        most_common_value = f'{top_left["label"]} ({top_left["pct"]}%)' if top_left else "N/A"

    # ── Bottom Two-Column Layout ──────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        # Left Distribution Panel
        bars_html = ""
        colors = ["bar-blue", "bar-red", "bar-orange", "bar-purple", "bar-teal"]
        for i, item in enumerate(left_items):
            bars_html += render_bar(item["label"], item["pct"], colors[i % len(colors)])

        st.html(f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">{left_title}</div>
            </div>
            {bars_html}
        </div>
        """)

        # Cross-cutting issues
        cc = get_cross_cutting(filtered_events)
        cc_rows = ""
        for item in cc:
            trend_color = "#E53935" if item["trend"] == "Increasing" else "#43A047" if item["trend"] == "Decreasing" else "#64748b"
            cc_rows += f"""
            <div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f1f5f9;">
                <div style="font-size:0.88rem;color:#334155;font-weight:500;"><span class="dot-blue"></span>{item["pair"]}</div>
                <div style="display:flex;align-items:center;gap:10px;">
                    <span style="font-weight:700;color:#1e293b;">{item["count"]}</span>
                    <span style="font-size:0.78rem;color:{trend_color};font-weight:600;">{item["trend"]}</span>
                </div>
            </div>
            """
        st.html(f"""
        <div class="card card-purple">
            <div class="card-header">
                <div class="card-title">Cross-Cutting Issues</div>
            </div>
            {cc_rows}
        </div>
        """)

    with col_right:
        # Severity Breakdown bar chart
        st.html("""
        <div class="card">
            <div class="card-header">
                <div class="card-title">Severity Breakdown</div>
            </div>
        </div>
        """)
        st.bar_chart(severity_df.set_index("Period"), use_container_width=True)

        # Right Distribution Panel
        right_bars = ""
        r_colors = ["bar-blue", "bar-teal", "bar-green", "bar-orange", "bar-purple", "bar-red"]
        for i, item in enumerate(right_dist_items):
            right_bars += render_bar(item["label"], item["pct"], r_colors[i % len(r_colors)])

        st.html(f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">{right_dist_title}</div>
            </div>
            {right_bars}
        </div>
        """)

        # Dynamic Analysis Summary
        summary = compute_trend_analysis_summary(trends_df, root_causes, action_trends)
        fastest_color = "#E53935"
        improving_color = "#43A047"
        st.html(f"""
        <div class="card card-green">
            <div class="card-header">
                <div class="card-title">Analysis Summary</div>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div>
                    <div class="summary-label">{most_common_label}</div>
                    <div class="summary-value">{most_common_value}</div>
                </div>
                <div>
                    <div class="summary-label">Fastest Growing</div>
                    <div class="summary-value" style="color:{fastest_color};">{summary["fastest_growing"]}</div>
                </div>
                <div>
                    <div class="summary-label">Top Action Type</div>
                    <div class="summary-value">{summary["top_action"]}</div>
                </div>
                <div>
                    <div class="summary-label">Improving Area</div>
                    <div class="summary-value" style="color:{improving_color};">{summary["improving_area"]}</div>
                </div>
            </div>
        </div>
        """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: WORKFLOW MONITOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Workflow Monitor":
    st.markdown("## Workflow Monitor")

    filters = get_global_filters()
    followups = apply_global_filters(get_incomplete_followups(), filters)
    wf = get_workflow_summary(followups)

    if not followups:
        st.info("No follow-ups match the current filters.")

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.html(render_kpi(wf["closed_with_gaps"], "Closed w/ Gaps", "urgent", "kpi-border-red"))
    with k2:
        st.html(render_kpi(wf["review_needed"], "Review Needed", "warn", "kpi-border-orange"))
    with k3:
        st.html(render_kpi(wf["complete"], "Complete", "ok", "kpi-border-green"))
    with k4:
        st.html(render_kpi(wf["total_analyzed"], "Total Analyzed", "primary", "kpi-border-blue"))

    st.html("<div style='height:0.75rem'></div>")

    # Incomplete Follow-ups Table

    fu_rows = ""
    for f in followups:
        urg_badge = render_severity_badge(f["urgency"])
        status_cls = "badge-red" if "Gap" in f["status"] else "badge-orange"
        fu_rows += f"""
        <tr>
            <td><strong>{f["file_id"]}</strong></td>
            <td><span class="badge {status_cls}">{f["status"]}</span></td>
            <td style="text-align:center;font-weight:600;">{f["pending"]}</td>
            <td style="text-align:center;font-weight:600;color:{"#E53935" if f["unanswered"]>0 else "#43A047"};">{f["unanswered"]}</td>
            <td>{urg_badge}</td>
            <td style="font-weight:700;">{f["urgency_count"]} {f["urgency"]}</td>
        </tr>
        """

    st.html(f"""
    <div class="card card-orange">
        <div class="card-header">
            <div class="card-title">Incomplete Follow-ups</div>
            <span class="badge badge-orange">{len(followups)} Events</span>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>File ID</th>
                    <th>Status</th>
                    <th style="text-align:center;">Pending</th>
                    <th style="text-align:center;">Unanswered</th>
                    <th>Urgency</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>{fu_rows}</tbody>
        </table>
    </div>
    """)

    # Expandable detail per follow-up
    st.html("""
    <div class="card">
        <div class="card-title" style="margin-bottom:0.75rem;">Follow-up Details</div>
    </div>
    """)

    for f in followups:
        with st.expander(f"FILE ID: {f['file_id']} — {f['status']} ({f['urgency_count']} {f['urgency']})"):
            items_html = ""
            for item in f["items"]:
                icon_cls = "dot-red" if item["level"] == "HIGH" else "dot-orange"
                items_html += f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <span class="{icon_cls}"></span>
                    <span class="badge {"badge-red" if item["level"]=="HIGH" else "badge-orange"}">{item["level"]}</span>
                    <span style="font-size:0.88rem;color:#334155;">{item["desc"]}</span>
                </div>
                """
            st.html(f"""
            <div style="padding:0.5rem 0;">
                <div class="summary-label" style="margin-bottom:0.75rem;">INCOMPLETE ITEMS</div>
                {items_html}
            </div>
            """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6: TAXONOMY REFERENCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Taxonomy Reference":

    # ── Header ────────────────────────────────────────────────────────────
    hdr_l, hdr_r = st.columns([3, 1])
    with hdr_l:
        st.markdown("## Taxonomy Reference")
    with hdr_r:
        st.html('<div style="text-align:right;padding-top:0.8rem;font-size:0.78rem;color:#64748b;">Last Updated: Dec 31 2025, 06:00 AM</div>')

    st.html("""
    <div style="background:#E3F2FD;border-radius:10px;padding:0.85rem 1.25rem;margin-bottom:1rem;display:flex;align-items:center;gap:10px;">
        <span style="font-size:1.3rem;">📚</span>
        <span style="font-size:0.88rem;color:#1565C0;">This taxonomy defines the standard categories used to classify patient safety events. Categories are applied automatically by the AI engine and validated by safety analysts.</span>
    </div>
    """)

    # ── Datix → New Taxonomy Crosswalk ────────────────────────────────────
    st.html('<div style="font-size:1.1rem;font-weight:700;color:#1e293b;margin:1rem 0 0.5rem 0;">Datix → New Taxonomy Crosswalk <span style="font-size:0.78rem;font-weight:400;color:#64748b;">(How legacy categories map forward)</span></div>')

    st.html("""
    <div style="background:#E8F5E9;border-radius:10px;padding:0.85rem 1.25rem;margin-bottom:1rem;display:flex;align-items:center;gap:10px;">
        <span style="font-size:1.3rem;">🔄</span>
        <span style="font-size:0.88rem;color:#2E7D32;">This crosswalk shows how familiar Datix categories (EVENT_TYPE, SPECIFIC_EVENT_TYPE_REPORTED) map to the new AI-derived taxonomy. The AI engine applies these mappings automatically — no manual re-coding is needed.</span>
    </div>
    """)

    crosswalk = get_datix_crosswalk()
    cw_rows = ""
    for group in crosswalk:
        sec_chips = " ".join(
            f'<span style="background:#F3E5F3;color:#7B1FA2;padding:2px 8px;border-radius:10px;font-size:0.75rem;white-space:nowrap;">{s}</span>'
            for s in group["secondaries"]
        )
        for i, m in enumerate(group["mappings"]):
            is_first = i == 0
            is_last = i == len(group["mappings"]) - 1
            # Visual grouping: remove top border on continuation rows, thicker bottom on last row
            td_border = "border-top:none;" if not is_first else ""
            td_bottom = "border-bottom:2px solid #e2e8f0;" if is_last else ""
            td_style = td_border + td_bottom
            primary_html = f'<span style="background:#E3F2FD;color:#1565C0;padding:2px 10px;border-radius:12px;font-size:0.82rem;font-weight:600;">{group["new_primary_category"]}</span>' if is_first else ""
            sec_html = f'<div style="display:flex;flex-wrap:wrap;gap:4px;">{sec_chips}</div>' if is_first else ""
            cw_rows += f"""
        <tr>
            <td style="color:#64748b;font-size:0.84rem;{td_style}">{m['datix_general']}</td>
            <td style="color:#64748b;font-size:0.84rem;{td_style}">{m['datix_specific']}</td>
            <td style="font-weight:600;color:#1e293b;border-left:3px solid #E3F2FD;padding-left:12px;{td_style}">{primary_html}</td>
            <td style="{td_style}">{sec_html}</td>
        </tr>
            """
    st.html(f"""
    <div class="card">
        <table class="data-table">
            <thead>
                <tr>
                    <th colspan="2" style="text-align:center;background:#f8fafc;color:#64748b;font-size:0.82rem;border-bottom:2px solid #e2e8f0;">Legacy Datix</th>
                    <th colspan="2" style="text-align:center;background:#E3F2FD;color:#1565C0;font-size:0.82rem;border-bottom:2px solid #90CAF9;">New Taxonomy</th>
                </tr>
                <tr>
                    <th>Datix General <div style="font-size:0.68rem;font-weight:400;color:#94a3b8;">EVENT_TYPE</div></th>
                    <th>Datix Specific <div style="font-size:0.68rem;font-weight:400;color:#94a3b8;">SPECIFIC_EVENT_TYPE_REPORTED</div></th>
                    <th>Primary Category</th>
                    <th>Secondaries <div style="font-size:0.68rem;font-weight:400;color:#94a3b8;">Clinical subcategories</div></th>
                </tr>
            </thead>
            <tbody>{cw_rows}</tbody>
        </table>
    </div>
    """)

    # ── Section 1: Primary Categories ─────────────────────────────────────
    st.html('<div style="font-size:1.1rem;font-weight:700;color:#1e293b;margin:1rem 0 0.5rem 0;">Primary Categories <span style="font-size:0.78rem;font-weight:400;color:#64748b;">(What went wrong)</span></div>')

    primary_cats = get_taxonomy_primary_categories()
    show_all = st.checkbox("Show all categories", value=False, key="tax_show_all")
    visible_cats = primary_cats if show_all else primary_cats[:4]

    c1, c2 = st.columns(2)
    for idx, cat in enumerate(visible_cats):
        col = c1 if idx % 2 == 0 else c2
        with col:
            with st.expander(f"{cat['name']}  —  {cat['usage_pct']}%", expanded=False):
                st.html(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
                        <span style="font-size:0.72rem;font-weight:700;color:#64748b;text-transform:uppercase;">Usage</span>
                        <span style="font-size:0.82rem;font-weight:700;color:{cat['color']};">{cat['usage_pct']}%</span>
                    </div>
                    <div style="background:#f1f5f9;border-radius:6px;height:8px;overflow:hidden;">
                        <div style="width:{cat['usage_pct']}%;height:100%;border-radius:6px;background:{cat['color']};"></div>
                    </div>
                </div>
                <div style="font-size:0.85rem;color:#334155;margin-bottom:6px;">{cat['description']}</div>
                <div style="font-size:0.72rem;font-weight:600;color:#64748b;text-transform:uppercase;margin-bottom:2px;">Examples</div>
                <div style="font-size:0.82rem;color:#475569;font-style:italic;">{cat['examples']}</div>
                """)

    # ── Section 2: Root Causes ────────────────────────────────────────────
    st.html('<div style="font-size:1.1rem;font-weight:700;color:#1e293b;margin:1.25rem 0 0.5rem 0;">Root Causes <span style="font-size:0.78rem;font-weight:400;color:#64748b;">(Why it happened)</span></div>')

    root_causes = get_taxonomy_root_causes()
    rc_rows = ""
    for rc in root_causes:
        rc_rows += f"""
        <tr>
            <td style="font-weight:600;color:#1e293b;">{rc['cause']}</td>
            <td style="font-size:0.84rem;color:#475569;">{rc['description']}</td>
            <td style="width:140px;">
                <div style="display:flex;align-items:center;gap:6px;">
                    <div style="flex:1;background:#f1f5f9;border-radius:4px;height:6px;overflow:hidden;">
                        <div style="width:{rc['usage_pct']}%;height:100%;border-radius:4px;background:{rc['color']};"></div>
                    </div>
                    <span style="font-size:0.78rem;font-weight:700;color:#334155;min-width:28px;text-align:right;">{rc['usage_pct']}%</span>
                </div>
            </td>
        </tr>
        """
    st.html(f"""
    <div class="card">
        <table class="data-table">
            <thead><tr><th>Root Cause</th><th>Description</th><th>Usage %</th></tr></thead>
            <tbody>{rc_rows}</tbody>
        </table>
    </div>
    """)

    # ── Section 3: Action Categories ──────────────────────────────────────
    st.html('<div style="font-size:1.1rem;font-weight:700;color:#1e293b;margin:1.25rem 0 0.5rem 0;">Action Categories</div>')

    act_left, act_right = st.columns(2)

    # 3a — Global Actions
    with act_left:
        actions = get_taxonomy_actions()
        act_rows = ""
        for a in actions:
            act_rows += f"""
            <tr>
                <td style="font-weight:600;color:#1e293b;">{a['category']}</td>
                <td style="font-size:0.84rem;color:#475569;">{a['description']}</td>
                <td style="width:120px;">
                    <div style="display:flex;align-items:center;gap:6px;">
                        <div style="flex:1;background:#f1f5f9;border-radius:4px;height:6px;overflow:hidden;">
                            <div style="width:{a['usage_pct']}%;height:100%;border-radius:4px;background:{a['color']};"></div>
                        </div>
                        <span style="font-size:0.78rem;font-weight:700;color:#334155;min-width:28px;text-align:right;">{a['usage_pct']}%</span>
                    </div>
                </td>
            </tr>
            """
        st.html(f"""
        <div class="card">
            <div class="card-header"><div class="card-title">Global Actions</div></div>
            <table class="data-table">
                <thead><tr><th>Category</th><th>Description</th><th>Usage %</th></tr></thead>
                <tbody>{act_rows}</tbody>
            </table>
        </div>
        """)

    # 3b — Event-Specific Actions
    with act_right:
        evt_actions = get_taxonomy_event_specific_actions()
        evt_cards = ""
        evt_colors = {"Nutrition / Feeding": "#2196F3", "IV / Vascular Access": "#FF9800",
                      "Medication Error": "#9C27B0", "Fall": "#009688"}
        for evt_name, items in evt_actions.items():
            color = evt_colors.get(evt_name, "#1E88E5")
            chips = " ".join(
                f'<span style="display:inline-block;background:{color}14;color:{color};font-size:0.78rem;font-weight:600;padding:3px 10px;border-radius:20px;margin:2px 2px;">{item}</span>'
                for item in items
            )
            evt_cards += f"""
            <div style="margin-bottom:10px;">
                <div style="font-size:0.82rem;font-weight:700;color:#1e293b;margin-bottom:4px;">{evt_name}</div>
                <div>{chips}</div>
            </div>
            """
        st.html(f"""
        <div class="card">
            <div class="card-header"><div class="card-title">Event-Specific Actions</div></div>
            {evt_cards}
        </div>
        """)

    # ── Section 4: Cross-Cutting Patterns ─────────────────────────────────
    st.html('<div style="font-size:1.1rem;font-weight:700;color:#1e293b;margin:1.25rem 0 0.5rem 0;">Cross-Cutting Patterns</div>')

    cross = get_taxonomy_cross_cutting()
    cx_rows = ""
    for c in cross:
        cx_rows += f"""
        <tr>
            <td style="font-weight:600;color:#1e293b;">{c['pattern']}</td>
            <td style="text-align:center;">{c['nutrition']}</td>
            <td style="text-align:center;">{c['iv_vascular']}</td>
            <td style="text-align:center;">{c['medication']}</td>
            <td style="text-align:center;font-weight:700;color:#1e293b;">{c['total']}</td>
        </tr>
        """
    st.html(f"""
    <div class="card">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Pattern</th>
                    <th style="text-align:center;">Nutrition</th>
                    <th style="text-align:center;">IV/Vascular</th>
                    <th style="text-align:center;">Medication</th>
                    <th style="text-align:center;">Total</th>
                </tr>
            </thead>
            <tbody>{cx_rows}</tbody>
        </table>
    </div>
    """)

    # Insight callout
    st.html("""
    <div style="background:#FFF9C4;border-radius:10px;padding:0.85rem 1.25rem;margin-top:0.5rem;display:flex;align-items:flex-start;gap:10px;">
        <span style="font-size:1.2rem;line-height:1;">💡</span>
        <span style="font-size:0.88rem;color:#424242;"><strong>Process + System Gap</strong> is the #1 cross-cutting pattern, appearing in <strong>28 events</strong> this period. Units with the highest overlap: Cardiac ICU (12) and Surgical (9). Consider a joint process-improvement initiative across these units.</span>
    </div>
    """)


# ══════════════════════════════════════════════════════════════════════════════
# LIAISON PAGE 1: MY EVENTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "My Events":
    ctx = get_liaison_context()
    st.markdown(f"## My Events — {ctx['header_suffix']}")

    filters = get_global_filters()
    all_events = get_event_list()
    filtered_events = apply_global_filters(all_events, filters)
    unit_events = filter_events_by_territory(filtered_events, ctx["liaison"], ctx["selected_floor"])

    if not unit_events:
        st.info("No events match the current filters for this unit.")

    # KPIs
    total_events = len(unit_events)
    open_events = sum(1 for e in unit_events if e.get("status") != "Closed")
    with_gaps = sum(1 for e in unit_events if e.get("gaps", 0) > 0)
    high_sev = sum(1 for e in unit_events if e.get("severity") == "High")
    med_sev = sum(1 for e in unit_events if e.get("severity") == "Medium")

    mk1, mk2, mk3, mk4 = st.columns(4)
    with mk1:
        st.html(render_kpi(total_events, "Total Events", "primary", "kpi-border-blue"))
    with mk2:
        st.html(render_kpi(open_events, "Open", "warn", "kpi-border-orange"))
    with mk3:
        st.html(render_kpi(with_gaps, "With Gaps", "urgent", "kpi-border-red"))
    with mk4:
        sev_text = f"{high_sev}H / {med_sev}M"
        st.html(render_kpi(sev_text, "Severity Split", "primary", "kpi-border-purple"))

    st.html("<div style='height:0.75rem'></div>")

    # Unit Events Table
    evt_rows = ""
    for e in unit_events:
        sev_badge = render_severity_badge(e["severity"])
        status_cls = "badge-orange" if "Review" in e["status"] else "badge-red" if "Escalat" in e["status"] else "badge-green"
        evt_rows += f"""
        <tr>
            <td><strong>{e["file_id"]}</strong></td>
            <td><span class="chip">{e["event_type"]}</span></td>
            <td>{e["date"]}</td>
            <td style="text-align:center;font-weight:600;">{e["problems"]}</td>
            <td style="text-align:center;font-weight:600;color:{"#E53935" if e["gaps"]>0 else "#43A047"};">{e["gaps"]}</td>
            <td>{sev_badge}</td>
            <td><span class="badge {status_cls}">{e["status"]}</span></td>
        </tr>
        """

    st.html(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title">Unit Events</div>
            <span class="badge badge-blue">{total_events} events</span>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>File ID</th>
                    <th>Type</th>
                    <th>Date</th>
                    <th>Problems</th>
                    <th>Gaps</th>
                    <th>Severity</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>{evt_rows}</tbody>
        </table>
    </div>
    """)


# ══════════════════════════════════════════════════════════════════════════════
# LIAISON PAGE 2: FOLLOW-UP WORKSPACE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Follow-Up Workspace":
    ctx = get_liaison_context()
    st.markdown(f"## Follow-Up Workspace — {ctx['header_suffix']}")

    filters = get_global_filters()
    all_events = get_event_list()
    filtered_events = apply_global_filters(all_events, filters)
    unit_events = filter_events_by_territory(filtered_events, ctx["liaison"], ctx["selected_floor"])

    # Only show events that need attention (not Closed, or have gaps)
    actionable = [e for e in unit_events if e.get("status") != "Closed" or e.get("gaps", 0) > 0]

    if actionable:
        st.html(f"""
        <div style="background:#FFF3E0;border-radius:10px;padding:0.75rem 1.25rem;margin-bottom:1rem;display:flex;align-items:center;gap:10px;">
            <span style="font-size:1.2rem;">&#9888;</span>
            <span style="font-size:0.88rem;color:#E65100;font-weight:600;">{len(actionable)} event(s) need attention in {ctx['header_suffix']}</span>
        </div>
        """)
    else:
        st.info("No events currently need follow-up attention in this unit.")

    if actionable:
        # Event selector
        event_options = [f"{e['file_id']} — {e['event_type']} ({e['date']}) — {e['status']}" for e in actionable]
        selected_label = st.selectbox("Select Event", event_options, key="followup_event_select")
        selected_idx = event_options.index(selected_label)
        event = actionable[selected_idx]

        # ── Top row: Narrative + Metadata ─────────────────────────────
        st.html(f"""
        <div class="card card-purple">
            <div class="card-header">
                <div class="card-title">Event Narrative: {event["file_id"]}</div>
                {render_severity_badge(event["severity"])}
            </div>
            <div class="narrative">{event["narrative"]}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;margin-top:0.75rem;">
                <div><div class="summary-label">DATE</div><div class="summary-value">{event["date"]}</div></div>
                <div><div class="summary-label">LOCATION</div><div class="summary-value">{event["location"]}</div></div>
                <div><div class="summary-label">PROBLEMS</div><div class="summary-value">{event["problems"]}</div></div>
                <div><div class="summary-label">GAPS</div><div class="summary-value" style="color:{"#E53935" if event["gaps"]>0 else "#43A047"};">{event["gaps"]}</div></div>
            </div>
        </div>
        """)

        # ── Two-column layout ─────────────────────────────────────────
        ws_left, ws_right = st.columns(2)

        with ws_left:
            # Chart Review Checklist — derived programmatically
            has_narrative = bool(event.get("narrative"))
            has_problems = len(event.get("problems_detail", [])) > 0
            has_root_cause = any(p.get("category") for p in event.get("problems_detail", []))
            has_suggested = len(event.get("suggested_actions", [])) > 0
            has_followups = len(event.get("actual_followups", [])) > 0
            has_gaps = event.get("gaps", 0) > 0 or len(event.get("gaps_detail", [])) > 0

            checklist_items = [
                ("Narrative reviewed", has_narrative),
                ("Problems categorized", has_problems),
                ("Root cause assessed", has_root_cause),
                ("Actions suggested", has_suggested),
                ("Follow-ups documented", has_followups),
                ("Gaps identified", has_gaps),
            ]
            check_html = ""
            for label, done in checklist_items:
                cls = "check-item check-done" if done else "check-item check-miss"
                check_html += f'<div class="{cls}">{label}</div>'

            st.html(f"""
            <div class="card">
                <div class="card-title" style="margin-bottom:0.75rem;">Chart Review Checklist</div>
                {check_html}
            </div>
            """)

            # Root Cause Assessment
            problems_html = ""
            for i, p in enumerate(event.get("problems_detail", []), 1):
                problems_html += f"""
                <div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;">
                    <div style="min-width:22px;height:22px;border-radius:50%;background:#1E88E5;color:#fff;font-size:0.72rem;font-weight:700;display:flex;align-items:center;justify-content:center;">{i}</div>
                    <div>
                        <div style="font-size:0.88rem;color:#1e293b;">{p["problem"]}</div>
                        <div><span class="chip">{p["category"]}</span></div>
                    </div>
                </div>
                """
            st.html(f"""
            <div class="card">
                <div class="card-title" style="margin-bottom:0.75rem;">Root Cause Assessment</div>
                {problems_html if problems_html else '<div style="font-size:0.85rem;color:#64748b;">No problems documented</div>'}
            </div>
            """)

        with ws_right:
            # Actions Taken
            followups_html = ""
            for f in event.get("actual_followups", []):
                followups_html += f"""
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                    <span class="badge badge-blue">{f["type"]}</span>
                    <span style="font-size:0.88rem;color:#334155;">{f["action"]}</span>
                </div>
                """
            # AI-Recommended Actions
            suggested_html = ""
            for s in event.get("suggested_actions", []):
                suggested_html += f'<div style="font-size:0.85rem;color:#475569;margin-bottom:4px;"><span class="dot-blue"></span>{s}</div>'

            st.html(f"""
            <div class="card card-green">
                <div class="card-title" style="margin-bottom:0.75rem;">Actions Taken</div>
                {followups_html if followups_html else '<div style="font-size:0.85rem;color:#64748b;">No follow-ups documented</div>'}
                <div style="margin-top:1rem;">
                    <div class="summary-label" style="margin-bottom:0.5rem;">AI-RECOMMENDED ACTIONS</div>
                    {suggested_html if suggested_html else '<div style="font-size:0.85rem;color:#64748b;">No suggestions</div>'}
                </div>
            </div>
            """)

            # Gaps & Outstanding
            gaps_html = ""
            for g in event.get("gaps_detail", []):
                gaps_html += f'<div style="font-size:0.85rem;color:#991b1b;margin-bottom:4px;"><span class="dot-red"></span>{g}</div>'
            if not event.get("gaps_detail"):
                gaps_html = '<div style="font-size:0.85rem;color:#43A047;"><span class="dot-green"></span>No gaps identified</div>'

            st.html(f"""
            <div class="card card-red">
                <div class="card-title" style="margin-bottom:0.75rem;">Gaps & Outstanding</div>
                {gaps_html}
            </div>
            """)

            # Completeness Score
            matched, total, pct = compute_completeness_score(event)
            st.html(f"""
            <div class="card">
                <div class="card-title" style="margin-bottom:0.75rem;">Completeness Score</div>
                {render_completeness_score(matched, total, pct)}
            </div>
            """)


# ══════════════════════════════════════════════════════════════════════════════
# LIAISON PAGE 3: DEPARTMENT TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Department Trends":
    ctx = get_liaison_context()
    st.markdown(f"## Department Trends — {ctx['header_suffix']}")

    filters = get_global_filters()
    all_events = get_event_list()
    filtered_events = apply_global_filters(all_events, filters)
    unit_events = filter_events_by_territory(filtered_events, ctx["liaison"], ctx["selected_floor"])

    if not unit_events:
        st.info("No events match the current filters for this unit.")

    # Controls
    dt_c1, dt_c2 = st.columns(2)
    with dt_c1:
        dept_view = st.selectbox("View", ["Event Types", "Clinical Subcategories", "Root Causes", "Action Types"], key="dept_trend_view")
    with dt_c2:
        dept_period = st.selectbox("Period", ["Weekly", "Monthly", "Quarterly"], key="dept_trend_period")

    if dept_view == "Clinical Subcategories":
        dept_topn_option = st.selectbox("Show", ["Top 5", "Top 10", "All"], index=1, key="dept_trend_topn")
    else:
        dept_topn_option = "All"

    # Fetch data scoped to unit events
    if dept_view == "Event Types":
        dept_trends_df = get_event_type_time_trends(unit_events, period=dept_period)
        dept_chart_title = f"Event Type Trends — {ctx['header_suffix']}"
    elif dept_view == "Clinical Subcategories":
        dept_trends_df = get_clinical_subcategory_time_trends(unit_events, period=dept_period)
        dept_chart_title = f"Clinical Subcategory Trends — {ctx['header_suffix']}"
    elif dept_view == "Root Causes":
        dept_trends_df = get_root_cause_time_trends(unit_events, period=dept_period)
        dept_chart_title = f"Root Cause Trends — {ctx['header_suffix']}"
    else:  # Action Types
        dept_trends_df = get_action_type_time_trends(unit_events, period=dept_period)
        dept_chart_title = f"Action Type Trends — {ctx['header_suffix']}"

    dept_kpi_label = {
        "Event Types": "Total Events",
        "Clinical Subcategories": "Total Subcategory Events",
        "Root Causes": "Total Root Causes",
        "Action Types": "Total Actions",
    }[dept_view]

    if dept_view == "Clinical Subcategories" and dept_topn_option != "All":
        n = int(dept_topn_option.split()[1])
        dept_numeric_cols_all = [c for c in dept_trends_df.columns if c != "Period"]
        dept_last_vals = {c: dept_trends_df[c].iloc[-1] for c in dept_numeric_cols_all}
        dept_top_cols = sorted(dept_last_vals, key=dept_last_vals.get, reverse=True)[:n]
        dept_trends_df = dept_trends_df[["Period"] + dept_top_cols]

    dept_severity_df = get_severity_time_trends(unit_events, period=dept_period)

    # KPIs
    dept_numeric_cols = [c for c in dept_trends_df.columns if c != "Period"]
    dept_total_last = int(dept_trends_df[dept_numeric_cols].iloc[-1].sum()) if len(dept_trends_df) > 0 else 0

    cat_summary = get_category_summary(unit_events)
    top_cat = cat_summary[0]["category"] if cat_summary else "N/A"

    dk1, dk2, dk3 = st.columns(3)
    with dk1:
        st.html(render_kpi(len(unit_events), "Unit Events", "primary", "kpi-border-blue"))
    with dk2:
        st.html(render_kpi(dept_total_last, dept_kpi_label, "primary", "kpi-border-purple"))
    with dk3:
        st.html(render_kpi(top_cat, "Top Category", "primary", "kpi-border-orange"))

    # Main Stacked Area Chart
    st.html(f"""
    <div class="card">
        <div class="card-header">
            <div class="card-title">{dept_chart_title}</div>
        </div>
    </div>
    """)
    st.area_chart(dept_trends_df.set_index("Period"), use_container_width=True)

    st.html("<div style='height:0.5rem'></div>")

    # ── View-aware left panel data ─────────────────────────────────────────
    dept_root_causes = get_root_cause_distribution(unit_events)
    dept_action_trends = get_action_trends(unit_events)

    if dept_view == "Event Types":
        dept_tax_cats = get_taxonomy_primary_categories()
        dept_left_title = "Event Type Distribution"
        dept_left_items = [{"label": c["name"], "pct": c["usage_pct"]} for c in dept_tax_cats]
    elif dept_view == "Clinical Subcategories":
        dept_ccs = get_clinical_category_summary(unit_events)
        dept_flat = []
        for _parent, data in dept_ccs.items():
            for c in data["categories"]:
                dept_flat.append({"label": c["category"], "count": c["count"]})
        dept_total_count = sum(item["count"] for item in dept_flat) or 1
        dept_left_items = [{"label": item["label"], "pct": int(round(item["count"] / dept_total_count * 100))}
                          for item in sorted(dept_flat, key=lambda x: x["count"], reverse=True)]
        dept_left_title = "Subcategory Distribution"
    elif dept_view == "Root Causes":
        dept_left_title = "Root Cause Distribution"
        dept_left_items = [{"label": rc["cause"], "pct": rc["pct"]} for rc in dept_root_causes]
    else:  # Action Types
        dept_left_title = "Action Type Distribution"
        dept_left_items = [{"label": at["action_type"], "pct": at["pct"]} for at in dept_action_trends]

    # Bottom Two-Column Layout
    dept_left, dept_right = st.columns(2)

    with dept_left:
        dept_bars_html = ""
        dept_colors = ["bar-blue", "bar-red", "bar-orange", "bar-purple", "bar-teal"]
        for i, item in enumerate(dept_left_items):
            dept_bars_html += render_bar(item["label"], item["pct"], dept_colors[i % len(dept_colors)])
        st.html(f"""
        <div class="card">
            <div class="card-header">
                <div class="card-title">{dept_left_title}</div>
            </div>
            {dept_bars_html}
        </div>
        """)

    with dept_right:
        st.html("""
        <div class="card">
            <div class="card-header">
                <div class="card-title">Severity Breakdown</div>
            </div>
        </div>
        """)
        st.bar_chart(dept_severity_df.set_index("Period"), use_container_width=True)


# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Safety Intelligence Dashboard v0.2 — Mock Data Mode. "
    "Snowflake views (DIA_GOLD_AI.RLDATIX.*) are stubbed and ready for wiring."
)
