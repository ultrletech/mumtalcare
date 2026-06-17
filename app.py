import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load('ppd_model.pkl')

# ── Language content ──────────────────────────────────────────────
content = {
    "English": {
        "title": "Mumtal Care",
        "subtitle": "Postpartum Depression Risk Screener",
        "description": "For use by midwives and community health workers. Enter the mother's details below to assess her PPD risk.",
        "lang_label": "Language / Kasa",
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
        "btn": "Assess Risk",
        "low_title": "🟢 Low Risk",
        "med_title": "🟡 Medium Risk — Monitor Closely",
        "high_title": "🔴 High Risk — Refer Now",
        "low_action": "Continue routine postnatal care. Check in again at next scheduled visit.",
        "med_action": "Schedule a follow-up visit within 1 week. Discuss support systems with the mother. Consider referral if symptoms worsen.",
        "high_action": "Refer to the nearest mental health officer or psychiatric nurse today. Do not leave mother alone. Alert a trusted family member if available.",
        "factors_title": "Key risk factors identified:",
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
        "no_factors": "No major individual risk factors — combined pattern suggests elevated risk.",
        "footer": "Mumtal Care is a screening tool only. It does not replace clinical diagnosis.",
    },
    "Twi": {
        "title": "Mumtal Care",
        "subtitle": "Dea Wohwɛ Sɛ Ɔba Awoo Akyi Adwene Yareɛ",
        "description": "Yei yɛ adwuma ma amammere ne akomhyɛfoɔ. Fa maame no ho nsɛm ka ase wɔ ase no so na mihwɛ ne keka.",
        "lang_label": "Language / Kasa",
        "section": "Maame No Ho Nsɛm",
        "q1": "Maame no mfeɛ (mfeɛ)",
        "q2": "Aware anaa mpaapaemu ho tebea",
        "q2_opts": ["Aware mfiri / Onni ɔkunu/okunu", "Aware / Wɔ ɔkunu/okunu"],
        "q3": "Ɔkunu anaa abusua ho mmoa",
        "q3_opts": ["Mmoa biara nni hɔ", "Kakra", "Saa saa", "Mmoa paa"],
        "q4": "Ɛyɛ sɛ wɔbɔɔ bo sɛ wɔbɛwo ba no anaa?",
        "q4_opts": ["Daabi", "Yiw"],
        "q5": "Wɔ adwene yareɛ anaa awerɛhoɔ ho asɛm daa?",
        "q5_opts": ["Daabi", "Yiw"],
        "q6": "Ɔwo ba a ɔwuu anaa awoɔ a enni mmerɛ daa?",
        "q6_opts": ["Daabi", "Yiw"],
        "q7": "Ba no si dɛn?",
        "q7_opts": ["Si papa", "Si ketewa"],
        "q8": "Maame no adwene tebea nnansa yi mu (nnahwere 2)",
        "q8_opts": ["Yaw paa", "Yaw", "Saa saa", "Ɛyɛ"],
        "q9": "Onne da yiye sɛnea ɛsɛ (gye sɛ ba no ma)",
        "q9_opts": ["Yaw paa", "Yaw", "Saa saa"],
        "q10": "Nnahwere sɛnea wɔwo ba no akyi",
        "q10_opts": ["0–2 nnahwere", "3–6 nnahwere", "6–12 nnahwere", "Nnahwere 12+"],
        "btn": "Hwɛ Keka",
        "low_title": "🟢 Keka Ketewa",
        "med_title": "🟡 Keka Mfinimfini — Hwɛ Yiye",
        "high_title": "🔴 Keka Kɛseɛ — Fa No Kɔ Okurufo Nkyɛn Seesei",
        "low_action": "Toa so na fa maame no hwɛ sɛnea ɛsɛ. San bɛhwɛ no bere a ɛsɛ so.",
        "med_action": "Bɛhwɛ no nnansa baako mu. Kasa ne no fa mmoa ho. Sɛ ne tebea yɛ dɛn a, fa no kɔ okurufo nkyɛn.",
        "high_action": "Fa no kɔ adwene yareɛ okurufo nkyɛn seesei. Mma no nkɔ nkoa. Ka kyerɛ ne mma a wɔwɔ hɔ.",
        "factors_title": "Keka a wɔhuu:",
        "factors": {
            "age": "Maame no mfeɛ sua (afe 20 ase)",
            "marital": "Onni ɔkunu/okunu anaa mmoa",
            "support": "Ɔkunu/abusua mmoa nni hɔ",
            "planned": "Awoɔ a wɔnbɔ bo faako",
            "mental": "Adwene yareɛ ho asɛm daa",
            "loss": "Ɔwo ba a ɔwuu daa",
            "lbw": "Ba a osi ketewa",
            "mood": "Adwene tebea bone",
            "sleep": "Onne da yiye koraa",
            "weeks": "Awoɔ akyi bere titiriw (nnahwere 0–6)",
        },
        "no_factors": "Keka titiriw biara nnhuu — tebea no kyerɛ keka.",
        "footer": "Mumtal Care yɛ hwɛ adwuma nko. Enka okyerɛkyerɛfo yareɛ ho nhyehyɛe.",
    }
}

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(page_title="Mumtal Care", page_icon="🤱", layout="centered")

# ── Language selector ─────────────────────────────────────────────
lang = st.selectbox("Language / Kasa", ["English", "Twi"])
c = content[lang]

# ── Header ────────────────────────────────────────────────────────
st.title(c["title"])
st.subheader(c["subtitle"])
st.write(c["description"])
st.divider()

# ── Input form ────────────────────────────────────────────────────
st.subheader(c["section"])

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

# ── On button click ───────────────────────────────────────────────
if st.button(c["btn"], type="primary", use_container_width=True):

    # Convert inputs to numbers the model understands
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

    st.divider()

    # Show result
    if prediction == 0:
        st.success(c["low_title"])
        st.write(c["low_action"])
    elif prediction == 1:
        st.warning(c["med_title"])
        st.write(c["med_action"])
    else:
        st.error(c["high_title"])
        st.write(c["high_action"])

    # Show contributing risk factors
    st.subheader(c["factors_title"])
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

    if found_factors:
        for f in found_factors:
            st.write(f"• {f}")
    else:
        st.write(c["no_factors"])

    st.divider()
    st.caption(c["footer"])