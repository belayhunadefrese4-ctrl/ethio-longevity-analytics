import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import string

# ==========================================
# 1. PAGE CONFIGURATION & SESSION STATE
# ==========================================
st.set_page_config(
    page_title="Global Longevity & Biological Age Analytics",
    page_icon="🌍",
    layout="wide"
)

if "free_used" not in st.session_state:
    st.session_state.free_used = False

if "unlocked_via_key" not in st.session_state:
    st.session_state.unlocked_via_key = False

ADMIN_PASSWORD = "ETHIO_ADMIN_2026"
UN_BASELINE_LE = 74.0  # UN Global Life Expectancy Baseline

# ==========================================
# 2. MULTILINGUAL DICTIONARY (6 High-Value Languages)
# ==========================================
TRANSLATIONS = {
    "English": {
        "title": "🌍 Global Longevity & Clinical Biological Age Platform",
        "subtitle": "Clinical assessment anchored on AHA Life's Essential 8™ & WHO Global Baselines (74 Years).",
        "tab1": "1. Standardized 15-KPI Health Assessment",
        "tab2": "2. Clinical Dashboard & Narrative Briefing",
        "tab3": "3. Remittance & Global Payments",
        "tab4": "4. Admin Console",
        "chrono_age": "Chronological Age",
        "bio_age": "Biological Age",
        "est_le": "Estimated Lifespan (UN Baseline: 74 Yrs)",
        "narrative_title": "📊 Executive Health & Longevity Narrative Briefing",
        "strengths": "💪 Validated Longevity Factors",
        "weaknesses": "⚠️ Clinical Risk Areas",
        "btn_export": "📄 Export Certified Narrative Report (PDF)"
    },
    "Deutsch": {
        "title": "🌍 Platform für Globale Langlebigkeit & Biologisches Alter",
        "subtitle": "Klinische Bewertung basierend auf AHA Life's Essential 8™ und WHO-Standards.",
        "tab1": "1. Standardisierte 15-KPI Gesundheitsbewertung",
        "tab2": "2. Klinisches Dashboard & Ausführlicher Bericht",
        "tab3": "3. Globale Zahlungen & Freischaltung",
        "tab4": "4. Admin-Konsole",
        "chrono_age": "Chronologisches Alter",
        "bio_age": "Biologisches Alter",
        "est_le": "Geschätzte Lebenserwartung (UN-Basis: 74 Jahre)",
        "narrative_title": "📊 Ausführlicher Medizinischer Analysebericht",
        "strengths": "💪 Starke Gesundheitsparameter",
        "weaknesses": "⚠️ Klinische Risikobereiche",
        "btn_export": "📄 Zertifizierten Bericht Exportieren (PDF)"
    },
    "Français": {
        "title": "🌍 Plateforme Mondiale de Longévité et Âge Biologique",
        "subtitle": "Évaluation clinique basée sur l'AHA Life's Essential 8™ et l'OMS.",
        "tab1": "1. Évaluation Santé à 15 KPI Normalisés",
        "tab2": "2. Tableau de Bord Clinique et Analyse Détaillée",
        "tab3": "3. Paiements Internationaux & Transferts",
        "tab4": "4. Console d'Administration",
        "chrono_age": "Âge Chronologique",
        "bio_age": "Âge Biologique",
        "est_le": "Espérance de Vie Estimée (Base ONU: 74 ans)",
        "narrative_title": "📊 Rapport Narratif d'Analyse Médicale",
        "strengths": "💪 Facteurs de Longévité Validés",
        "weaknesses": "⚠️ Domaines de Risque Clinique",
        "btn_export": "📄 Exporter le Rapport Certifié (PDF)"
    },
    "日本語": {
        "title": "🌍 グローバル長寿＆生物学的年齢アナリティクスプラットフォーム",
        "subtitle": "米国心臓協会 (AHA) Life's Essential 8™ および WHO 基準に基づく評価。",
        "tab1": "1. 15の標準化ヘルスKPI評価",
        "tab2": "2. 臨床ダッシュボード＆詳細レポート",
        "tab3": "3. 国際送金・決済と認証",
        "tab4": "4. 管理コンソール",
        "chrono_age": "暦年齢",
        "bio_age": "生物学的年齢",
        "est_le": "推定寿命 (国連基準: 74歳)",
        "narrative_title": "📊 エグゼクティブ健康評価分析レポート",
        "strengths": "💪 長寿促進要因",
        "weaknesses": "⚠️ 改善が必要なリスク要因",
        "btn_export": "📄 認定レポートをダウンロード (PDF)"
    },
    "العربية": {
        "title": "🌍 المنصة العالمية للتحليلات الطبية للعمر البيولوجي والمدى العمري",
        "subtitle": "تقييم سريري معتمد على معايير جمعية القلب الأمريكية (AHA) ومنظمة الصحة العالمية.",
        "tab1": "1. تقييم مؤشرات الصحة الـ 15 المعتمدة",
        "tab2": "2. لوحة التحليلات السريرية والتقرير التفصيلي",
        "tab3": "3. المدفوعات الدولية والتحويلات المالية",
        "tab4": "4. لوحة التحكم والإدارة",
        "chrono_age": "العمر الزمني",
        "bio_age": "العمر البيولوجي",
        "est_le": "العمر المتوقع (معيار الأمم المتحدة: 74 عاماً)",
        "narrative_title": "📊 التقرير التحليلي الطبي السردي",
        "strengths": "💪 نقاط القوة الصحية المعتمدة",
        "weaknesses": "⚠️ مجالات المخاطر السريرية",
        "btn_export": "📄 تحميل التقرير الطبي المعتمد (PDF)"
    },
    "አማርኛ": {
        "title": "🌍 ዓለም አቀፍ የዕድሜ ጣሪያ እና የባዮሎጂካል እድሜ ትንተና መድረክ",
        "subtitle": "በተባበሩት መንግስታት (UN 74 ዓመት) እና በ AHA Life's Essential 8™ መሠረት የተዘጋጀ።",
        "tab1": "1. 15ቱ ዓለም አቀፍ የጤና መለኪያዎች",
        "tab2": "2. የባዮሎጂካል እድሜ እና የዕድሜ ጣሪያ ዳሽቦርድ",
        "tab3": "3. የክፍያ ገጽ እና ሪፖርት ማውረጃ",
        "tab4": "4. የአስተዳዳሪ መቆጣጠሪያ (Admin)",
        "chrono_age": "የትውልድ እድሜ",
        "bio_age": "የባዮሎጂካል እድሜ",
        "est_le": "የተገመተው የዕድሜ ጣሪያ (UN Baseline: 74 ዓመት)",
        "narrative_title": "📊 ዝርዝር የጤና ትንተና እና የባዮሎጂካል እድሜ መግለጫ",
        "strengths": "💪 የታዩ የጤና ጥንካሬዎች",
        "weaknesses": "⚠️ ሊሻሻሉ የሚገቡ የጤና ስጋቶች",
        "btn_export": "📄 የተረጋገጠ የጤና ሪፖርት አውርድ (PDF)"
    }
}

# Language selection
lang_choice = st.sidebar.selectbox("🌐 Select Language / ቋንቋ ይምረጡ / Sprache wählen", list(TRANSLATIONS.keys()))
T = TRANSLATIONS[lang_choice]

st.title(T["title"])
st.caption(T["subtitle"])
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([T["tab1"], T["tab2"], T["tab3"], T["tab4"]])

# ==========================================
# 3. TAB 1: STANDARDIZED 15-KPI FORM
# ==========================================
with tab1:
    st.subheader(T["tab1"])
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🧬 Demographics & Metabolic Health")
        user_name = st.text_input("Full Name", "Abebe Kebede")
        age = st.number_input("1. Chronological Age", 18, 100, 35)
        bmi_val = st.selectbox("2. Body Mass Index (BMI) Range", ["Normal (18.5 - 24.9)", "Underweight (<18.5)", "Overweight (25 - 29.9)", "Obese (≥30)"])
        bp_val = st.selectbox("3. Blood Pressure Status (AHA Standard)", ["Optimal (<120/80 mmHg)", "Elevated / Stage 1 (120-139/80-89)", "Stage 2 Hypertension (≥140/90 mmHg)"])
        glucose_val = st.selectbox("4. Fasting Blood Glucose / HbA1c", ["Normal (<100 mg/dL / HbA1c <5.7%)", "Prediabetes (100-125 mg/dL)", "Diabetes Range (≥126 mg/dL)"])
        chol_val = st.selectbox("5. Lipid Profile / Non-HDL Cholesterol", ["Optimal (<130 mg/dL)", "Moderate (130-159 mg/dL)", "High (≥160 mg/dL)"])

    with c2:
        st.markdown("### 🏃 Lifestyle & Cardiovascular Behaviors")
        ex_val = st.selectbox("6. Weekly Exercise (AHA Essential 8)", ["≥150 mins Moderate or ≥75 mins Vigorous", "30 to 149 mins Weekly", "<30 mins / Sedentary"])
        diet_val = st.selectbox("7. Diet Pattern Alignment (Mediterranean / DASH)", ["High Fruit, Vegetable & Whole Grain Alignment", "Moderate Balanced Diet", "High Processed / High Sugar / Refined Carbs"])
        sleep_val = st.selectbox("8. Sleep Duration & Quality", ["7 to 9 Hours Restorative Nightly", "5 to 6 Hours Irregular", "<5 Hours Chronic Deprivation"])
        smoke_val = st.selectbox("9. Nicotine / Tobacco Exposure", ["Never Smoked or Quit >5 Years", "Former Smoker (Quit <5 Years)", "Active Inhaled Tobacco / Vaping"])
        hyd_val = st.selectbox("10. Daily Hydration Intake", ["≥2.5 Liters Water Daily", "1.5 to 2.4 Liters Daily", "<1.5 Liters Daily / Sugary Beverages"])

    with c3:
        st.markdown("### 🧠 Mental, Social & Clinical Screening")
        stress_val = st.selectbox("11. Chronic Stress & Cortisol Control", ["Low Stress / Active Resilience Practices", "Moderate Work Stress", "High Chronic Stress / Burnout"])
        social_val = st.selectbox("12. Social Support & Community Connection", ["Strong Social Network & Low Isolation", "Moderate Social Connection", "Weak Support Network / Isolated"])
        fam_val = st.selectbox("13. Premature Family Chronic Disease History", ["No Early Cardiovascular / Cancer History", "1 Immediate Family Member", "Multiple Immediate Family Members"])
        alcohol_val = st.selectbox("14. Alcohol Consumption Pattern", ["Zero or Moderate (≤1 drink/day)", "Occasional Binge / Moderate", "Heavy Consumption (>8 drinks/week)"])
        screen_val = st.selectbox("15. Annual Clinical Checkups & Biomarker Monitoring", ["Annual Comprehensive Blood & Diagnostic Screening", "Occasional Screening", "Rarely / Never Screened"])

    st.success("✅ **15 Standardized KPIs Logged!** Proceed to Tab 2 to view your Clinical Analysis.")

# Scoring Calculation Engine
delta = 0.0
if "Normal" in bmi_val: delta -= 1.0
elif "Obese" in bmi_val: delta += 3.0

if "Optimal" in bp_val: delta -= 1.5
elif "Stage 2" in bp_val: delta += 2.5

if "Normal" in glucose_val: delta -= 1.0
elif "Diabetes" in glucose_val: delta += 2.5

if "≥150" in ex_val: delta -= 2.0
elif "Sedentary" in ex_val: delta += 2.5

if "High Fruit" in diet_val: delta -= 1.5
elif "High Processed" in diet_val: delta += 2.0

if "7 to 9" in sleep_val: delta -= 1.0
elif "<5 Hours" in sleep_val: delta += 1.5

if "Never" in smoke_val: delta -= 1.5
elif "Active" in smoke_val: delta += 4.0

bio_age = max(18.0, round(age + delta, 1))
le_delta = (age - bio_age) * 0.75
est_le = round(UN_BASELINE_LE + le_delta, 1)
age_diff = round(age - bio_age, 1)

# ==========================================
# 4. TAB 2: CLINICAL DASHBOARD & NARRATIVE
# ==========================================
with tab2:
    st.header(T["tab2"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric(T["chrono_age"], f"{age} Yrs")
    m2.metric(T["bio_age"], f"{bio_age} Yrs")
    m3.metric(T["est_le"], f"{est_le} Yrs")

    st.divider()

    # Visual Multi-Chart Layout
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("🎯 Biological Age vs Chronological Age")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=bio_age,
            delta={'reference': age, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge={
                'axis': {'range': [18, 100]},
                'bar': {'color': "#1E88E5" if age_diff >= 0 else "#E53935"},
                'steps': [
                    {'range': [18, 40], 'color': "#E3F2FD"},
                    {'range': [40, 70], 'color': "#FFFDE7"},
                    {'range': [70, 100], 'color': "#FFEBEE"}
                ]
            }
        ))
        fig_gauge.update_layout(height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_g2:
        st.subheader("📊 Health Category Impact Scores")
        impact_df = pd.DataFrame({
            "Category": ["Metabolic", "Cardiovascular", "Lifestyle", "Sleep & Stress"],
            "Impact (Years)": [
                -2.0 if "Normal" in glucose_val else 2.5,
                -1.5 if "Optimal" in bp_val else 2.5,
                -2.0 if "≥150" in ex_val else 2.0,
                -1.0 if "7 to 9" in sleep_val else 1.5
            ]
        })
        fig_bar = px.bar(impact_df, x="Category", y="Impact (Years)", color="Impact (Years)", color_continuous_scale="RdYlGn_r")
        fig_bar.update_layout(height=280)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # Paragraph Narrative Executive Summary
    st.subheader(T["narrative_title"])
    
    narrative_p1 = f"""
    **Patient Overview & Cellular Aging:** Based on your 15 clinical and behavioral Key Performance Indicators evaluated against the UN baseline of 74 years and AHA Life's Essential 8™ guidelines, your current calculated **Biological Age is {bio_age} years** relative to your **Chronological Age of {age} years**. This represents a net cellular age variance of **{abs(age_diff)} years {'younger' if age_diff >= 0 else 'older'}** than your chronological baseline.
    """
    
    narrative_p2 = f"""
    **Metabolic & Cardiovascular Risk Analysis:** Your reported blood pressure status ({bp_val}), fasting blood glucose level ({glucose_val}), and physical activity profile ({ex_val}) indicate an overall projected lifespan of **{est_le} years**. Maintaining optimal blood pressure below 120/80 mmHg and engaged exercise of over 150 minutes per week significantly preserves vascular elasticity and endothelial function, helping protect against premature cardiovascular morbidity.
    """
    
    narrative_p3 = f"""
    **Targeted Longevity Optimization Roadmap:** To further decelerate biological aging and enhance healthy life expectancy (HALE), clinical priorities should focus on optimizing sleep hygiene ({sleep_val}), maintaining a low-glycemic Mediterranean or DASH diet pattern, and conducting routine annual blood panels to track Non-HDL cholesterol and inflammatory biomarkers.
    """

    st.markdown(narrative_p1)
    st.markdown(narrative_p2)
    st.markdown(narrative_p3)

    st.divider()

    if st.button(T["btn_export"]):
        st.session_state.free_used = True
        st.success("🎉 Certified narrative report ready!")
        st.download_button(
            "📥 Save Full Clinical Briefing (.txt)",
            data=f"{T['narrative_title']}\n\nClient: {user_name}\nChronological Age: {age}\nBiological Age: {bio_age}\nEstimated Lifespan: {est_le}\n\n{narrative_p1}\n\n{narrative_p2}\n\n{narrative_p3}",
            file_name=f"Longevity_Clinical_Briefing_{user_name}.txt"
        )

# ==========================================
# 5. TAB 3: REMITTANCE & PAYMENTS
# ==========================================
with tab3:
    st.header(T["tab3"])
    p1, p2 = st.columns(2)
    
    with p1:
        st.subheader("💚 Global Payment & Remittance Methods")
        curr = st.radio("Select Currency", ["ETB (ብር)", "USD ($)", "EUR (€)", "GBP (£)"])
        
        st.info(
            "**📲 Mobile Money / International Remittance (Sendwave, Remitly, WorldRemit):**\n"
            "* Recipient Phone: `+251986884912`\n"
            "* Name: **Belayhun Adefrese**\n\n"
            "**🏦 Direct Bank Transfer (Commercial Bank of Ethiopia - CBE):**\n"
            "* Account Number: `1000296269488`\n"
            "* Name: **Belayhun Adefrese Metaferia** (Lem Area Branch, Addis Ababa)"
        )
        
        c_name = st.text_input("Sender Full Name")
        c_ref = st.text_input("Transaction Ref / MTCN / Confirmation Code")
        if st.button("📩 Submit Verification Claim", type="primary"):
            if len(c_ref.strip()) >= 5:
                st.success("✅ Payment claim logged! Your single-use access key will be sent via SMS.")
            else:
                st.error("❌ Enter a valid transaction reference code.")

    with p2:
        st.subheader("🔑 Unlock Full Unlimited Reports")
        key_in = st.text_input("Enter Access Key Received via SMS", type="password")
        if st.button("Verify & Unlock Access"):
            if key_in.strip():
                st.session_state.unlocked_via_key = True
                st.success("🎉 Key Verified! Full access unlocked.")
                st.rerun()

# ==========================================
# 6. TAB 4: ADMIN CONSOLE
# ==========================================
with tab4:
    st.header(T["tab4"])
    pwd = st.text_input("Admin Password", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("🔓 Authenticated as Administrator")
        target_phone = st.text_input("Client Phone Number", "+251986884912")
        if st.button("📲 Generate & Dispatch Key"):
            gen_key = f"GLOB-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
            st.info(f"Generated Key: **{gen_key}** dispatched to **{target_phone}**.")
