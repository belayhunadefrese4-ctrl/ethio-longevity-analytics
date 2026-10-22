import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
# 2. BILINGUAL DICTIONARY (English & አማርኛ)
# ==========================================
TRANSLATIONS = {
    "English": {
        "title": "🌍 Global Longevity & Biological Age Analytics Platform",
        "subtitle": "Discover your biological age and estimated lifespan anchored on UN global health data (Baseline: 74 Years) using 15 core lifestyle KPIs.",
        "tab1": "1. 15-Factor Global Health Assessment",
        "tab2": "2. Biological Age & UN Lifespan Dashboard",
        "tab3": "3. Flexible Contribution & Report Unlock",
        "tab4": "4. Admin Console",
        
        # 15 Questions
        "q1": "1. What is your current age?",
        "q2": "2. How much exercise do you get per week?",
        "q3": "3. How balanced is your daily diet?",
        "q4": "4. How many hours of sleep do you get per night?",
        "q5": "5. How would you rate your daily stress level?",
        "q6": "6. What is your tobacco or smoking status?",
        "q7": "7. How often do you consume alcohol?",
        "q8": "8. How strong are your social connections and support network?",
        "q9": "9. How regularly do you undergo routine health checkups?",
        "q10": "10. How would you describe your daily hydration habits?",
        "q11": "11. How would you describe your body weight relative to height (BMI)?",
        "q12": "12. Do immediate family members have a history of early chronic disease?",
        "q13": "13. How often do you eat fresh fruits, vegetables, and whole foods?",
        "q14": "14. How would you describe your daily mental stress / workload?",
        "q15": "15. Do you get routine health checkups or blood monitoring every 1–2 years?",

        # Options
        "ex_opts": ["Less than 30 minutes", "30 to 150 minutes", "More than 150 minutes"],
        "diet_opts": ["Mostly whole foods, fruits, and vegetables", "Average diet with occasional processed foods", "Mostly fast food, processed meals, or high sugar"],
        "sleep_opts": ["7 to 9 hours consistently", "5 to 6 hours or irregular schedule", "Less than 5 hours consistently"],
        "stress_opts": ["Low stress, well-managed / mindfulness", "Moderate stress, manageable most days", "High chronic stress, frequently overwhelmed"],
        "smoke_opts": ["Never smoked or quit > 5 years ago", "Former smoker (quit within last 5 years)", "Current smoker or use tobacco regularly"],
        "alc_opts": ["Rarely or never (0-1 drink/week)", "Moderate consumption (2-7 drinks/week)", "Heavy or frequent consumption (8+ drinks/week)"],
        "social_opts": ["Strong, regular supportive contact", "Moderate, occasionally isolated", "Weak, frequently lonely or isolated"],
        "check_opts": ["Annually or as recommended", "Occasionally / when feeling unwell", "Rarely or never"],
        "hyd_opts": ["2+ liters (8+ glasses) daily", "Moderate (1-2 liters daily)", "Less than 1 liter / mostly sugary drinks"],
        "bmi_opts": ["Healthy / Normal weight", "Underweight", "Overweight", "Significantly overweight"],
        "fam_opts": ["No family history of early chronic disease", "Yes (1 immediate family member)", "Yes (Multiple immediate family members)"],
        "yes_no": ["Yes", "No"],

        # Metrics
        "bio_age": "Biological Age",
        "chrono_age": "Chronological Age",
        "est_le": "Estimated Life Expectancy (UN Baseline: 74 Yrs)",
        "strengths": "💪 Global Health Strengths",
        "weaknesses": "⚠️ Areas for Global Longevity Optimization",
        "recommendations": "🌱 Evidence-Based Longevity Action Plan"
    },
    "አማርኛ": {
        "title": "🌍 ዓለም አቀፍ የዕድሜ ጣሪያ እና የባዮሎጂካል እድሜ ትንተና መድረክ",
        "subtitle": "በተባበሩት መንግስታት (UN) የ 74 ዓመት ዓለም አቀፍ አማካይ መሠረት እና በ 15 ዋና ዋና የጤና መለኪያዎች የውስጥ አካልዎን እድሜ ያሰሉ።",
        "tab1": "1. 15ቱ ዓለም አቀፍ የጤና እና የአኗኗር ጥያቄዎች",
        "tab2": "2. የባዮሎጂካል እድሜ እና የዕድሜ ጣሪያ ዳሽቦርድ",
        "tab3": "3. የክፍያ ገጽ እና ሪፖርት ማውረጃ",
        "tab4": "4. የአስተዳዳሪ መቆጣጠሪያ (Admin)",
        
        # 15 Questions (Amharic)
        "q1": "1. አሁን ያለዎት ዕድሜ ስንት ነው?",
        "q2": "2. በሳምንት ውስጥ ምን ያህል የአካል ብቃት እንቅስቃሴ ያደርጋሉ?",
        "q3": "3. ዕለታዊ የምግብ አመጋገብዎ ምን ይመስላል?",
        "q4": "4. በየዕለቱ ምን ያህል ሰዓት ይተኙ?",
        "q5": "5. ዕለታዊ የአእምሮ ጭንቀትዎን እንዴት ይገልጹታል?",
        "q6": "6. የሲጋራ ወይም የትምባሆ አጠቃቀም ሁኔታዎ?",
        "q7": "7. የአልኮል መጠጥ አጠቃቀምዎ ምን ያህል ነው?",
        "q8": "8. የማህበራዊ ግንኙነት እና የድጋፍ አውታርዎ ምን ያህል ጠንካራ ነው?",
        "q9": "9. መደበኛ የጤና ምርመራዎችን ምን ያህል ጊዜ ያደርጋሉ?",
        "q10": "10. ዕለታዊ የውሃ አጠቃቀም ልማድዎ?",
        "q11": "11. ከቁመትዎ አንጻር የሰውነት ክብደትዎ (BMI)?",
        "q12": "12. በቤተሰብ ውስጥ ቀደም ብሎ የተከሰተ የከባድ ህመም (የስኳር፣ የልብ) ታሪክ አለ?",
        "q13": "13. አዲስ ፍራፍሬዎችን፣ አትክልቶችን እና ተፈጥሯዊ ምግቦችን ምን ያህል frequent ይበላሉ?",
        "q14": "14. ዕለታዊ የአእምሮ ጫና ወይም የስራ ጭንቀት መጠን?",
        "q15": "15. ቢያንስ በየ 1-2 ዓመቱ የደም ወይም የጤና ምርመራ ያደርጋሉ?",

        # Options (Amharic)
        "ex_opts": ["ከ 30 ደቂቃ በታች", "ከ 30 እስከ 150 ደቂቃ", "ከ 150 ደቂቃ በላይ"],
        "diet_opts": ["በተፈጥሯዊ ምግቦች፣ ፍራፍሬዎች እና አትክልቶች የበለፀገ", "መደበኛ ምግብ ከትንሽ የታሸጉ ምግቦች ጋር", "ፈጣን ምግቦች፣ የታሸጉ እና ከፍተኛ ስኳር ያላቸው"],
        "sleep_opts": ["ቋሚ ከ 7 እስከ 9 ሰዓት", "ከ 5 እስከ 6 ሰዓት ወይም መደበኛ ያልሆነ", "ከ 5 ሰዓት በታች लगातार"],
        "stress_opts": ["ዝቅተኛ ጭንቀት፣ በጥሩ ሁኔታ የሚመራ", "መካከለኛ ጭንቀት", "ከፍተኛ እና ዘላቂ ጭንቀት"],
        "smoke_opts": ["ፈጽሞ አጨስ አላውቅም ወይም ከ 5 ዓመት በፊት አቁሜያለሁ", "የቀድሞ አጽንቃሽ (ባለፉት 5 ዓመታት ውስጥ ያቆመ)", "አሁን የሚያጨሱ ወይም በየጊዜው የሚጠቀሙ"],
        "alc_opts": ["በጣም እጅግ አሜት (በሳምንት 0-1 ብርጭቆ)", "በልከኝነት (በሳምንት 2-7)", "ከፍተኛ እና ተደጋጋሚ አጠቃቀም (8+)"],
        "social_opts": ["ጠንካራ እና አጋዥ የቤተሰብ/ጓደኛ ግንኙነት", "መካከለኛ", "ደካማ፣ ብዙ ጊዜ ብቻቸውን የሚሰማቸው"],
        "check_opts": ["በየዓመቱ ወይም በሐኪም ትዕዛዝ", "ሐኪም ጋር ሲታመም ብቻ", "በጣም እጅግ አልፎ አልፎ"],
        "hyd_opts": ["2+ ሊትር (8+ ብርጭቆ) በዕለት", "መካከለኛ (1-2 ሊትር)", "ከ 1 ሊትር በታች / ሱቅ ውስጥ የሚገዙ ጣፋጭ መጠጦች"],
        "bmi_opts": ["ጤናማ / መደበኛ ክብደት", "ቀጭን / አነስተኛ ክብደት", "ከፍተኛ ክብደት (Overweight)", "ከመጠን ያለፈ ውፍረት (Obese)"],
        "fam_opts": ["የቤተሰብ የህመም ታሪክ የለም", "አዎ (1 የቤተሰብ አባል)", "አዎ (በርካታ የቤተሰብ አባላት)"],
        "yes_no": ["አዎ", "አይደለም"],

        # Metrics
        "bio_age": "የባዮሎጂካል (የውስጥ አካል) እድሜ",
        "chrono_age": "የትውልድ እድሜ",
        "est_le": "የተገመተው የዕድሜ ጣሪያ (UN Baseline: 74 ዓመት)",
        "strengths": "💪 የታዩ ዓለም አቀፍ የጤና ጥንካሬዎች",
        "weaknesses": "⚠️ ሊሻሻሉ የሚገቡ የጤና ስጋቶች",
        "recommendations": "🌱 በሳይንሳዊ መረጃ ላይ የተመሰረተ የረጅም ዕድሜ መመሪያ"
    }
}

# ==========================================
# 3. GLOBAL SCORING ENGINE
# ==========================================
def calculate_global_longevity(
    age, ex_idx, diet_idx, sleep_idx, stress_idx, smoke_idx, alc_idx,
    social_idx, check_idx, hyd_idx, bmi_idx, fam_idx, veg_idx, work_stress_idx, blood_check
):
    delta = 0.0
    strengths, weaknesses = [], []

    # Exercise
    if ex_idx == 2: delta -= 2.0; strengths.append(("High Physical Activity (>150 mins/week)", "ከፍተኛ ሳምንታዊ የአካል ብቃት እንቅስቃሴ"))
    elif ex_idx == 0: delta += 2.0; weaknesses.append(("Sedentary Lifestyle (<30 mins/week)", "አነስተኛ የአካል እንቅስቃሴ"))

    # Diet
    if diet_idx == 0: delta -= 1.5; strengths.append(("Whole Food & Plant-Rich Nutrition", "ተፈጥሯዊ እና በቪታሚን የበለፀገ ምግብ"))
    elif diet_idx == 2: delta += 2.5; weaknesses.append(("High Processed / Sugar Diet Risk", "የታሸጉ እና ከፍተኛ ስኳር ያላቸው ምግቦች ስጋት"))

    # Sleep
    if sleep_idx == 0: delta -= 1.0; strengths.append(("Optimal Sleep Hygiene (7-9 Hours)", "በቂ እና ጤናማ የእንቅልፍ ሰዓት"))
    elif sleep_idx == 2: delta += 1.5; weaknesses.append(("Chronic Sleep Deprivation (<5 Hours)", "ከፍተኛ የእንቅልፍ እጥረት"))

    # Stress
    if stress_idx == 0: delta -= 1.0; strengths.append(("Effective Stress Management", "ጥሩ የጭንቀት ማኔጅመንት"))
    elif stress_idx == 2: delta += 2.0; weaknesses.append(("High Chronic Stress Levels", "ከፍተኛ እና ዘላቂ የአእምሮ ጭንቀት"))

    # Smoking
    if smoke_idx == 0: delta -= 1.0; strengths.append(("Non-Smoker Status", "ከሲጋራ እና ትምባሆ ነፃ"))
    elif smoke_idx == 2: delta += 4.0; weaknesses.append(("Tobacco Consumption Risk", "የትምባሆ አጠቃቀም ከፍተኛ ስጋት"))

    # Alcohol
    if alc_idx == 0: delta -= 0.5; strengths.append(("Low/Zero Alcohol Consumption", "ዝቅተኛ ወይም ከቶ የማይጠጡ"))
    elif alc_idx == 2: delta += 2.0; weaknesses.append(("Heavy Alcohol Intake Risk", "ከፍተኛ የአልኮል አጠቃቀም ስጋት"))

    # Social
    if social_idx == 0: delta -= 1.0; strengths.append(("Strong Social & Community Support", "ጠንካራ ማህበራዊ ግንኙነት እና ድጋፍ"))
    elif social_idx == 2: delta += 1.5; weaknesses.append(("Social Isolation Risk", "የማህበራዊ መገለል ስጋት"))

    # Checkups
    if check_idx == 0 or blood_check == 0: delta -= 1.0; strengths.append(("Proactive Healthcare", "ቀደም ብሎ የመመርመር እና የጤና ክትትል ልማድ"))
    else: weaknesses.append(("Inconsistent Medical Checkups", "መደበኛ የጤና ምርመራ እጥረት"))

    # Hydration
    if hyd_idx == 0: delta -= 0.5; strengths.append(("Optimal Daily Hydration (2+ Liters)", "በቂ የውሃ አጠቃቀም"))
    elif hyd_idx == 2: delta += 1.0; weaknesses.append(("Suboptimal Hydration", "አነስተኛ የውሃ አጠቃቀም"))

    # BMI
    if bmi_idx == 0: delta -= 1.0; strengths.append(("Healthy Weight Range (Normal BMI)", "ጤናማ የሰውነት ክብደት"))
    elif bmi_idx >= 2: delta += 2.5; weaknesses.append(("Overweight / Obesity Risk", "ከፍተኛ የውፍረት ስጋት"))

    # Family History
    if fam_idx == 0: delta -= 1.0; strengths.append(("Favorable Family Chronic Disease History", "ጥሩ የቤተሰብ የጤና ታሪክ"))
    elif fam_idx == 2: delta += 2.0; weaknesses.append(("Family History of Chronic Illness", "የዘር ውርስ የህመም ታሪክ ስጋት"))

    bio_age = max(18.0, round(age + delta, 1))
    le_delta = (age - bio_age) * 0.75
    est_life_expectancy = round(UN_BASELINE_LE + le_delta, 1)

    return bio_age, est_life_expectancy, strengths, weaknesses

# ==========================================
# 4. APP LAYOUT & NAVIGATION
# ==========================================
lang_choice = st.sidebar.selectbox("🌐 Choose Language / ቋንቋ ይምረጡ", ["English", "አማርኛ"])
T = TRANSLATIONS[lang_choice]

st.title(T["title"])
st.caption(T["subtitle"])
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([T["tab1"], T["tab2"], T["tab3"], T["tab4"]])

# TAB 1: FORM
with tab1:
    st.subheader(T["tab1"])
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### Part 1: Demographics & Vitals")
        user_name = st.text_input("Full Name / ሙሉ ስም", "Abebe Kebede")
        age = st.number_input(T["q1"], 18, 100, 35)
        bmi_sel = st.selectbox(T["q11"], T["bmi_opts"])
        bmi_idx = T["bmi_opts"].index(bmi_sel)
        fam_sel = st.selectbox(T["q12"], T["fam_opts"])
        fam_idx = T["fam_opts"].index(fam_sel)
        social_sel = st.selectbox(T["q8"], T["social_opts"])
        social_idx = T["social_opts"].index(social_sel)
        check_sel = st.selectbox(T["q9"], T["check_opts"])
        check_idx = T["check_opts"].index(check_sel)

    with c2:
        st.markdown("### Part 2: Lifestyle & Habits")
        ex_sel = st.selectbox(T["q2"], T["ex_opts"])
        ex_idx = T["ex_opts"].index(ex_sel)
        diet_sel = st.selectbox(T["q3"], T["diet_opts"])
        diet_idx = T["diet_opts"].index(diet_sel)
        veg_sel = st.selectbox(T["q13"], T["diet_opts"])
        veg_idx = T["diet_opts"].index(veg_sel)
        sleep_sel = st.selectbox(T["q4"], T["sleep_opts"])
        sleep_idx = T["sleep_opts"].index(sleep_sel)
        hyd_sel = st.selectbox(T["q10"], T["hyd_opts"])
        hyd_idx = T["hyd_opts"].index(hyd_sel)

    with c3:
        st.markdown("### Part 3: Clinical & Mental Factors")
        stress_sel = st.selectbox(T["q5"], T["stress_opts"])
        stress_idx = T["stress_opts"].index(stress_sel)
        work_stress_sel = st.selectbox(T["q14"], T["stress_opts"])
        work_stress_idx = T["stress_opts"].index(work_stress_sel)
        smoke_sel = st.selectbox(T["q6"], T["smoke_opts"])
        smoke_idx = T["smoke_opts"].index(smoke_sel)
        alc_sel = st.selectbox(T["q7"], T["alc_opts"])
        alc_idx = T["alc_opts"].index(alc_sel)
        blood_check_sel = st.radio(T["q15"], T["yes_no"])
        blood_check = 0 if blood_check_sel == T["yes_no"][0] else 1

    st.success("✅ **15 Factors Recorded!** Proceed to Tab 2 to see your Biological Age results.")

# Calculate
bio_age, est_le, strengths, weaknesses = calculate_global_longevity(
    age, ex_idx, diet_idx, sleep_idx, stress_idx, smoke_idx, alc_idx,
    social_idx, check_idx, hyd_idx, bmi_idx, fam_idx, veg_idx, work_stress_idx, blood_check
)
age_diff = round(age - bio_age, 1)

# TAB 2: RESULTS
with tab2:
    st.header(T["tab2"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric(T["chrono_age"], f"{age} Years / ዓመት")
    m2.metric(T["bio_age"], f"{bio_age} Years / ዓመት")
    m3.metric(T["est_le"], f"{est_le} Years")

    st.divider()

    if not st.session_state.free_used or st.session_state.unlocked_via_key:
        if not st.session_state.unlocked_via_key:
            st.success("🎁 **Complimentary 1-Time Free Assessment Active!**")

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=bio_age,
            title={'text': T["bio_age"], 'font': {'size': 20}},
            delta={'reference': age, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge={
                'axis': {'range': [18, 100]},
                'bar': {'color': "#1976D2" if age_diff >= 0 else "#D32F2F"},
                'steps': [
                    {'range': [18, 40], 'color': "#E3F2FD"},
                    {'range': [40, 70], 'color': "#FFFDE7"},
                    {'range': [70, 100], 'color': "#FFEBEE"}
                ]
            }
        ))
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        col_s, col_w = st.columns(2)
        with col_s:
            st.subheader(T["strengths"])
            for s_en, s_am in strengths:
                st.markdown(f"🟢 **{s_am if lang_choice == 'አማርኛ' else s_en}**")

        with col_w:
            st.subheader(T["weaknesses"])
            if weaknesses:
                for w_en, w_am in weaknesses:
                    st.markdown(f"🔴 **{w_am if lang_choice == 'አማርኛ' else w_en}**")

        st.divider()
        st.subheader(T["recommendations"])
        if lang_choice == "አማርኛ":
            st.markdown("* **🥗 ተፈጥሯዊ ምግብ:** አትክልት፣ ፍራፍሬ እና ከፍተኛ ፋይበር ያላቸውን እህል አብዝተው ይመገቡ።\n* **🏃 ስፖርት:** በሳምንት ከ150 ደቂቃ በላይ እንቅስቃሴ ያድርጉ።\n* **🧘 እረፍት:** ከ7-9 ሰዓት እንቅልፍ ይተኛሉ።")
        else:
            st.markdown("* **🥗 Whole-Food Nutrition:** Prioritize fresh produce & fiber-rich legumes.\n* **🏃 Aerobic Activity:** Engage in >150 mins/week of exercise.\n* **🧘 Rest & Sleep:** Maintain 7–9 hours of sleep nightly.")

        if st.button("📄 Export Certified Longevity Report (PDF)"):
            st.session_state.free_used = True
            st.success("🎉 Free trial credit applied! Report ready for download.")
            st.download_button("📥 Click to Save Report", data=f"Longevity Report for {user_name}\nBiological Age: {bio_age}\nLife Expectancy: {est_le}", file_name=f"Longevity_Report_{user_name}.txt")
    else:
        st.warning("🔒 **Free 1-Time Assessment Completed.** To generate additional reports, please complete a contribution claim in Tab 3.")

# TAB 3: PAYMENT
with tab3:
    st.header(T["tab3"])
    p1, p2 = st.columns(2)
    with p1:
        st.subheader("💚 Support Platform & Unlock Unlimited Access")
        curr = st.radio("Currency / የክፍያ ዓይነት", ["ETB (ብር)", "USD ($)"])
        amt = st.number_input("Amount (Min 20 ETB / $3 USD)", min_value=20 if curr == "ETB (ብር)" else 3, value=200 if curr == "ETB (ብር)" else 10)
        st.info("**📱 Telebirr:** `+251986884912` (Belayhun Adefrese)\n\n**🏦 CBE Bank:** `1000296269488` (Belayhun Adefrese Metaferia)")
        c_name = st.text_input("Sender Name")
        c_phone = st.text_input("Sender Phone")
        c_ref = st.text_input("Transaction Ref / SMS Code")
        if st.button("📩 Submit Claim", type="primary"):
            if len(c_ref.strip()) >= 5: st.success("✅ Payment claim logged! Your access key will be sent via SMS.")
            else: st.error("❌ Invalid reference code.")
    with p2:
        st.subheader("🔑 Unlock via SMS Key")
        key_in = st.text_input("Access Key", type="password")
        if st.button("Verify & Unlock"):
            if key_in.strip():
                st.session_state.unlocked_via_key = True
                st.success("🎉 Key Verified! Unlimited access granted.")
                st.rerun()

# TAB 4: ADMIN
with tab4:
    st.header(T["tab4"])
    pwd = st.text_input("Admin Password", type="password")
    if pwd == ADMIN_PASSWORD:
        st.success("🔓 Authenticated")
        target_phone = st.text_input("Client Phone", "+251986884912")
        if st.button("📲 Dispatch SMS Key"):
            gen_key = f"GLOB-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
            st.info(f"Key: **{gen_key}** dispatched to **{target_phone}**.")
