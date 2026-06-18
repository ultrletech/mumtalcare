import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load('ppd_model.pkl')

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(page_title="Mumtal Care", page_icon="🤱", layout="centered")

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #fdf6f0 0%, #fef9f5 50%, #fdf0e8 100%);
}

.hero {
    background: linear-gradient(135deg, #8B4513 0%, #A0522D 40%, #CD853F 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(139, 69, 19, 0.25);
}
.hero-icon { font-size: 3rem; margin-bottom: 0.5rem; }
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.85);
    margin: 0.4rem 0 0;
    font-weight: 400;
    text-align: center;
}
.hero-desc {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.7);
    margin: 1rem auto 0;
    line-height: 1.6;
    max-width: 600px;
    text-align: center;
    white-space: nowrap;
}

.section-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 16px rgba(139, 69, 19, 0.08);
    border: 1px solid rgba(139, 69, 19, 0.08);
}
.section-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: #A0522D;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.2rem;
}

.result-low {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border-radius: 16px;
    padding: 1.5rem;
    border-left: 5px solid #16a34a;
    margin-bottom: 1rem;
}
.result-medium {
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    border-radius: 16px;
    padding: 1.5rem;
    border-left: 5px solid #d97706;
    margin-bottom: 1rem;
}
.result-high {
    background: linear-gradient(135deg, #fff1f2, #ffe4e6);
    border-radius: 16px;
    padding: 1.5rem;
    border-left: 5px solid #dc2626;
    margin-bottom: 1rem;
}
.result-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}
.result-low .result-title { color: #15803d; }
.result-medium .result-title { color: #b45309; }
.result-high .result-title { color: #dc2626; }
.result-action {
    font-size: 0.9rem;
    line-height: 1.6;
    color: #374151;
}

.factors-card {
    background: #fdf6f0;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
    border: 1px solid rgba(139, 69, 19, 0.12);
}
.factor-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 0;
    font-size: 0.875rem;
    color: #4B3A2A;
    border-bottom: 1px solid rgba(139,69,19,0.07);
}
.factor-item:last-child { border-bottom: none; }

.stats-bar {
    background: linear-gradient(135deg, #fff8f4, #fdf0e8);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    display: flex;
    justify-content: space-around;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(139, 69, 19, 0.1);
}
.stat-item { text-align: center; }
.stat-num {
    font-size: 1.4rem;
    font-weight: 700;
    color: #8B4513;
}
.stat-label {
    font-size: 0.7rem;
    color: #A0522D;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.footer {
    text-align: center;
    padding: 1.5rem;
    color: #9CA3AF;
    font-size: 0.75rem;
    line-height: 1.6;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-weight: 500 !important;
    color: #374151 !important;
    font-size: 0.9rem !important;
}

/* Red assess button */
.stButton button {
    background: linear-gradient(135deg, #c0392b, #e74c3c) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100% !important;
    box-shadow: 0 4px 16px rgba(192, 57, 43, 0.4) !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(192, 57, 43, 0.5) !important;
}

div[data-testid="stSelectbox"] > div,
div[data-testid="stNumberInput"] > div > div {
    border-radius: 10px !important;
    border-color: rgba(139, 69, 19, 0.2) !important;
}

/* Force dark dropdown menu with white text */
ul[role="listbox"],
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background-color: #1a1a2e !important;
}
ul[role="listbox"] li,
li[role="option"],
li[role="option"] span {
    color: #ffffff !important;
    background-color: #1a1a2e !important;
}
li[role="option"]:hover {
    background-color: #2d2d4a !important;
}
</style>
""", unsafe_allow_html=True)

# ── Content ───────────────────────────────────────────────────────
c = {
    "title": "Mumtal Care",
    "subtitle": "Postpartum Depression Risk Screener",
    "description": "A clinical screening tool for midwives & community health workers across Ghana.",
    "section": "Mother's Information",
    "q1": "Age of mother (years)",
    "q2": "Marital / relationship status",
    "q2_opts": ["Single / No partner", "Married / Has partner"],
    "q3": "Partner or family support level",
    "q3_opts": ["None", "Little", "Moderate", "Strong"],
    "q4": "Was the pregnancy planned?",
    "q4_opts": ["No", "Yes"],
    "q5": "Any history of depression or mental illness?",
    "q5_opts": ["No", "Yes"],
    "q6": "Previous miscarriage or pregnancy loss?",
    "q6_opts": ["No", "Yes"],
    "q7": "Baby's birth weight",
    "q7_opts": ["Normal birth weight", "Low birth weight"],
    "q8": "Mother's self-reported mood in past 2 weeks",
    "q8_opts": ["Very low", "Low", "Mostly okay", "Good"],
    "q9": "Sleep quality since birth (beyond normal baby disruptions)",
    "q9_opts": ["Very poor", "Poor", "Okay"],
    "q10": "Weeks since delivery",
    "q10_opts": ["0–2 weeks", "3–6 weeks", "6–12 weeks", "12+ weeks"],
    "btn": "🔍 Assess Risk",
    "low_title": "🟢 Low Risk",
    "med_title": "🟡 Medium Risk — Monitor Closely",
    "high_title": "🔴 High Risk — Refer Now",
    "low_action": "Continue routine postnatal care. Check in again at next scheduled visit.",
    "med_action": "Schedule a follow-up visit within 1 week. Discuss support systems with the mother. Consider referral if symptoms worsen.",
    "high_action": "Refer to the nearest mental health officer or psychiatric nurse today. Do not leave mother alone. Alert a trusted family member if available.",
    "factors_title": "⚠️ Key risk factors identified",
    "factors": {
        "age": "Young maternal age (under 20)",
        "marital": "No partner or relationship support",
        "support": "Low partner/family support",
        "planned": "Unplanned pregnancy",
        "mental": "Prior history of depression or mental illness",
        "loss": "Previous pregnancy loss",
        "lbw": "Low birth weight baby",
        "mood": "Low self-reported mood",
        "sleep": "Very poor sleep quality",
        "weeks": "Early postpartum period (0–6 weeks)",
    },
    "no_factors": "No single dominant risk factor — combined pattern suggests elevated risk.",
    "footer": "Mumtal Care is a clinical screening tool only and does not replace formal diagnosis.\nBuilt for Ghana · Powered by AI",
}

# ── Hero ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-icon">🤱</div>
    <h1 class="hero-title">{c["title"]}</h1>
    <p class="hero-subtitle">{c["subtitle"]}</p>
    <p class="hero-desc">{c["description"]}</p>
</div>
""", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-num">~29%</div>
        <div class="stat-label">Ghanaian Mothers Affected</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">10</div>
        <div class="stat-label">Risk Factors Assessed</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">82%</div>
        <div class="stat-label">Model Accuracy</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────
st.markdown(f'<div class="section-card"><p class="section-title">📋 {c["section"]}</p>', unsafe_allow_html=True)

age = st.number_input(c["q1"], min_value=13, max_value=55, value=25)
marital = st.selectbox(c["q2"], c["q2_opts"])
support = st.selectbox(c["q3"], c["q3_opts"])
planned = st.selectbox(c["q4"], c["q4_opts"])
mental = st.selectbox(c["q5"], c["q5_opts"])
loss = st.selectbox(c["q6"], c["q6_opts"])
lbw = st.selectbox(c["q7"], c["q7_opts"])
mood = st.selectbox(c["q8"], c["q8_opts"])
sleep = st.selectbox(c["q9"], c["q9_opts"])
weeks = st.selectbox(c["q10"], c["q10_opts"])

st.markdown('</div>', unsafe_allow_html=True)

# ── Assess button ─────────────────────────────────────────────────
assess = st.button(c["btn"], type="primary", use_container_width=True)

if assess:
    age_val = int(age)
    marital_val = 0 if marital == c["q2_opts"][0] else 1
    support_val = c["q3_opts"].index(support)
    planned_val = 0 if planned == c["q4_opts"][0] else 1
    mental_val = 0 if mental == c["q5_opts"][0] else 1
    loss_val = 0 if loss == c["q6_opts"][0] else 1
    lbw_val = 0 if lbw == c["q7_opts"][0] else 1
    mood_val = c["q8_opts"].index(mood)
    sleep_val = c["q9_opts"].index(sleep)
    weeks_val = c["q10_opts"].index(weeks)

    features = np.array([[age_val, marital_val, support_val, planned_val,
                          mental_val, loss_val, lbw_val, mood_val, sleep_val, weeks_val]])
    prediction = model.predict(features)[0]

    if prediction == 0:
        st.markdown(f"""
        <div class="result-low">
            <div class="result-title">{c["low_title"]}</div>
            <div class="result-action">{c["low_action"]}</div>
        </div>""", unsafe_allow_html=True)
    elif prediction == 1:
        st.markdown(f"""
        <div class="result-medium">
            <div class="result-title">{c["med_title"]}</div>
            <div class="result-action">{c["med_action"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-high">
            <div class="result-title">{c["high_title"]}</div>
            <div class="result-action">{c["high_action"]}</div>
        </div>""", unsafe_allow_html=True)

    found_factors = []
    if age_val < 20: found_factors.append(c["factors"]["age"])
    if marital_val == 0: found_factors.append(c["factors"]["marital"])
    if support_val < 2: found_factors.append(c["factors"]["support"])
    if planned_val == 0: found_factors.append(c["factors"]["planned"])
    if mental_val == 1: found_factors.append(c["factors"]["mental"])
    if loss_val == 1: found_factors.append(c["factors"]["loss"])
    if lbw_val == 1: found_factors.append(c["factors"]["lbw"])
    if mood_val < 2: found_factors.append(c["factors"]["mood"])
    if sleep_val == 0: found_factors.append(c["factors"]["sleep"])
    if weeks_val < 2: found_factors.append(c["factors"]["weeks"])

    factors_html = ""
    if found_factors:
        for f in found_factors:
            factors_html += f'<div class="factor-item">⚠️ {f}</div>'
    else:
        factors_html = f'<div class="factor-item">✅ {c["no_factors"]}</div>'

    st.markdown(f"""
    <div class="factors-card">
        <p class="section-title">{c["factors_title"]}</p>
        {factors_html}
    </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────
st.markdown(f'<div class="footer">{c["footer"]}</div>', unsafe_allow_html=True)