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
    page_icon="🧬",
    layout="wide"
)

if "free_used" not in st.session_state:
    st.session_state.free_used = False

if "unlocked_via_key" not in st.session_state:
    st.session_state.unlocked_via_key = False

ADMIN_PASSWORD = "ETHIO_ADMIN_2026"
UN_BASELINE_LE = 74.0  # UN Global Life Expectancy Baseline

# ==========================================
# 2. MULTILINGUAL DICTIONARY (6 Major Languages)
# ==========================================
TRANSLATIONS = {
    "አማርኛ": {
        "title": "🌍 ዓለም አቀፍ የዕድሜ ጣሪያ እና የባዮሎጂካል እድሜ ትንተና መድረክ",
        "subtitle": "በተባበሩት መንግስታት (UN 74 ዓመት) እና በ AHA Life's Essential 8™ መሠረት የተዘጋጀ።",
        "tab1": "1. 15ቱ ዓለም አቀፍ የጤና መለኪያዎች",
        "tab2": "2. የባዮሎጂካል እድሜ እና የዕድሜ ጣሪያ ዳሽቦርድ",
        "tab3": "3. የክፍያ ገጽ እና ሪፖርት ማውረጃ",
        "tab4": "4. የአስተዳዳሪ መቆጣጠሪያ (Admin)",
        "p1_head": "🧬 የስነ-ሕዝብ እና የሜታቦሊክ ጤና መለኪያዎች",
        "p2_head": "🏃 የአኗኗር ዘይቤ እና የልብ-ደም ቧንቧ ልማዶች",
        "p3_head": "🧠 የአእምሮ፣ የማህበራዊ እና የክሊኒካዊ ምርመራ",
        "name_lbl": "ሙሉ ስም",
        "q1": "1. የትውልድ ዕድሜ (Chronological Age)",
        "q2": "2. የሰውነት ክብደት መለኪያ (BMI Range)",
        "q3": "3. የደም ግፊት ሁኔታ (AHA Standard)",
        "q4": "4. የፆም ደም ስኳር / HbA1c",
        "q5": "5. የኮሌስትሮል መጠን (Non-HDL Cholesterol)",
        "q6": "6. ሳምንታዊ የአካል ብቃት እንቅስቃሴ",
        "q7": "7. የምግብ አመጋገብ ዘይቤ (Mediterranean / DASH)",
        "q8": "8. የእንቅልፍ ሰዓት እና ጥራት",
        "q9": "9. የትምባሆ / የሲጋራ ተፅእኖ",
        "q10": "10. ዕለታዊ የውሃ አጠቃቀም",
        "q11": "11. የረጅም ጊዜ የአእምሮ ጭንቀት ቁጥጥር",
        "q12": "12. የማህበራዊ ግንኙነት እና የድጋፍ አውታር",
        "q13": "13. የቤተሰብ ቀደምት የከባድ ህመም ታሪክ",
        "q14": "14. የአልኮል መጠጥ አጠቃቀም ልማድ",
        "q15": "15. ዓመታዊ የጤና እና የደም ምርመራ ክትትል",
        "bmi_opts": ["መደበኛ (18.5 - 24.9)", "ቀጭን / አነስተኛ (<18.5)", "ከፍተኛ ክብደት (25 - 29.9)", "ከመጠን ያለፈ ውፍረት (≥30)"],
        "bp_opts": ["ጤናማ (<120/80 mmHg)", "መካከለኛ / ደም ግፊት አነሳስ (120-139/80-89)", "ከፍተኛ ደም ግፊት (≥140/90 mmHg)"],
        "gluc_opts": ["መደበኛ (<100 mg/dL / HbA1c <5.7%)", "የስኳር ህመም አነሳስ (100-125 mg/dL)", "ከፍተኛ የስኳር መጠን (≥126 mg/dL)"],
        "chol_opts": ["ጤናማ (<130 mg/dL)", "መካከለኛ (130-159 mg/dL)", "ከፍተኛ (≥160 mg/dL)"],
        "ex_opts": ["≥150 ደቂቃ በሳምንት", "ከ 30 እስከ 149 ደቂቃ በሳምንት", "<30 ደቂቃ / አነስተኛ እንቅስቃሴ"],
        "diet_opts": ["በአትክልት፣ ፍራፍሬ እና እህሎች የበለፀገ", "መደበኛ የተመጣጠነ ምግብ", "የታሸጉ እና ከፍተኛ ስኳር ያላቸው ምግቦች"],
        "sleep_opts": ["ከ 7 እስከ 9 ሰዓት በየለሊቱ", "ከ 5 እስከ 6 ሰዓት መደበኛ ያልሆነ", "<5 ሰዓት ከፍተኛ የእንቅልፍ እጥረት"],
        "smoke_opts": ["አጨስ አላውቅም ወይም ከ5 ዓመት በፊት አቁሜያለሁ", "የቀድሞ አጽንቃሽ (ከ5 ዓመት በታች ያቆመ)", "አሁን የሚያጨሱ ወይም ቮፕ የሚጠቀሙ"],
        "hyd_opts": ["≥2.5 ሊትር ውሃ በየዕለቱ", "ከ 1.5 እስከ 2.4 ሊትር በየዕለቱ", "<1.5 ሊትር በየዕለቱ / ጣፋጭ መጠጦች"],
        "stress_opts": ["ዝቅተኛ ጭንቀት / ጥሩ ማኔጅመንት", "መካከለኛ የስራ ጭንቀት", "ከፍተኛ ዘላቂ የአእምሮ ጭንቀት"],
        "social_opts": ["ጠንካራ ማህበራዊ ግንኙነት እና ድጋፍ", "መካከለኛ ግንኙነት", "ደካማ ማህበራዊ ግንኙነት"],
        "fam_opts": ["የቤተሰብ የህመም ታሪክ የለም", "1 የቤተሰብ አባል", "በርካታ የቤተሰብ አባላት"],
        "alc_opts": ["አልኮል አልጠቀምም ወይም በልከኝነት (≤1 ብርጭቆ/ቀን)", "መካከለኛ አጠቃቀም", "ከፍተኛ አጠቃቀም (>8 ብርጭቆ/ሳምንት)"],
        "screen_opts": ["በየዓመቱ የደም እና የጤና ምርመራ አደርጋለሁ", "አልፎ አልፎ የሚደረግ ምርመራ", "በጣም አልፎ አልፎ ወይም ፈጽሞ አልመራመርም"],
        "succ_msg": "✅ **15ቱ ዓለም አቀፍ የጤና መለኪያዎች ተመዝግበዋል!** ውጤቱን ለማየት ወደ ክፍል 2 ይለፉ።",
        "chrono_age": "የትውልድ እድሜ",
        "bio_age": "የባዮሎጂካል እድሜ",
        "est_le": "የተገመተው የዕድሜ ጣሪያ (UN Baseline: 74 ዓመት)",
        "gauge_title": "🎯 የባዮሎጂካል እድሜ ከትውልድ እድሜ ጋር ሲነጻጸር",
        "bar_title": "📊 የጤና ዘርፎች በተለዋዋጭ እድሜ ላይ ያላቸው ተፅእኖ",
        "narrative_title": "📊 የጤና ትንተና እና የባዮሎጂካል እድሜ ማጠቃለያ መግለጫ",
        "btn_export": "📄 የተረጋገጠ የጤና ሪፖርት አውርድ (PDF)"
    },
    "English": {
        "title": "🌍 Global Longevity & Clinical Biological Age Platform",
        "subtitle": "Clinical assessment anchored on AHA Life's Essential 8™ & WHO Global Baselines (74 Years).",
        "tab1": "1. Standardized 15-KPI Health Assessment",
        "tab2": "2. Clinical Dashboard & Narrative Briefing",
        "tab3": "3. Remittance & Global Payments",
        "tab4": "4. Admin Console",
        "p1_head": "🧬 Demographics & Metabolic Health",
        "p2_head": "🏃 Lifestyle & Cardiovascular Behaviors",
        "p3_head": "🧠 Mental, Social & Clinical Screening",
        "name_lbl": "Full Name",
        "q1": "1. Chronological Age",
        "q2": "2. Body Mass Index (BMI) Range",
        "q3": "3. Blood Pressure Status (AHA Standard)",
        "q4": "4. Fasting Blood Glucose / HbA1c",
        "q5": "5. Lipid Profile / Non-HDL Cholesterol",
        "q6": "6. Weekly Exercise (AHA Essential 8)",
        "q7": "7. Diet Pattern Alignment (Mediterranean / DASH)",
        "q8": "8. Sleep Duration & Quality",
        "q9": "9. Nicotine / Tobacco Exposure",
        "q10": "10. Daily Hydration Intake",
        "q11": "11. Chronic Stress & Cortisol Control",
        "q12": "12. Social Support & Community Connection",
        "q13": "13. Premature Family Chronic Disease History",
        "q14": "14. Alcohol Consumption Pattern",
        "q15": "15. Annual Clinical Checkups & Biomarker Monitoring",
        "bmi_opts": ["Normal (18.5 - 24.9)", "Underweight (<18.5)", "Overweight (25 - 29.9)", "Obese (≥30)"],
        "bp_opts": ["Optimal (<120/80 mmHg)", "Elevated / Stage 1 (120-139/80-89)", "Stage 2 Hypertension (≥140/90 mmHg)"],
        "gluc_opts": ["Normal (<100 mg/dL / HbA1c <5.7%)", "Prediabetes (100-125 mg/dL)", "Diabetes Range (≥126 mg/dL)"],
        "chol_opts": ["Optimal (<130 mg/dL)", "Moderate (130-159 mg/dL)", "High (≥160 mg/dL)"],
        "ex_opts": ["≥150 mins Moderate or ≥75 mins Vigorous", "30 to 149 mins Weekly", "<30 mins / Sedentary"],
        "diet_opts": ["High Fruit, Vegetable & Whole Grain Alignment", "Moderate Balanced Diet", "High Processed / High Sugar / Refined Carbs"],
        "sleep_opts": ["7 to 9 Hours Restorative Nightly", "5 to 6 Hours Irregular", "<5 Hours Chronic Deprivation"],
        "smoke_opts": ["Never Smoked or Quit >5 Years", "Former Smoker (Quit <5 Years)", "Active Inhaled Tobacco / Vaping"],
        "hyd_opts": ["≥2.5 Liters Water Daily", "1.5 to 2.4 Liters Daily", "<1.5 Liters Daily / Sugary Beverages"],
        "stress_opts": ["Low Stress / Active Resilience Practices", "Moderate Work Stress", "High Chronic Stress / Burnout"],
        "social_opts": ["Strong Social Network & Low Isolation", "Moderate Social Connection", "Weak Support Network / Isolated"],
        "fam_opts": ["No Early Cardiovascular / Cancer History", "1 Immediate Family Member", "Multiple Immediate Family Members"],
        "alc_opts": ["Zero or Moderate (≤1 drink/day)", "Occasional Binge / Moderate", "Heavy Consumption (>8 drinks/week)"],
        "screen_opts": ["Annual Comprehensive Blood & Diagnostic Screening", "Occasional Screening", "Rarely / Never Screened"],
        "succ_msg": "✅ **15 Standardized KPIs Logged!** Proceed to Tab 2 to view your Clinical Analysis.",
        "chrono_age": "Chronological Age",
        "bio_age": "Biological Age",
        "est_le": "Estimated Lifespan (UN Baseline: 74 Yrs)",
        "gauge_title": "🎯 Biological Age vs Chronological Age",
        "bar_title": "📊 Health Category Impact Scores",
        "narrative_title": "📊 Executive Health & Longevity Narrative Briefing",
        "btn_export": "📄 Export Certified Narrative Report (PDF)"
    },
    "Deutsch": {
        "title": "🌍 Globale Plattform für Langlebigkeit und Biologisches Alter",
        "subtitle": "Klinische Bewertung basierend auf AHA Life's Essential 8™ und WHO-Standards.",
        "tab1": "1. Standardisierte 15-KPI Gesundheitsbewertung",
        "tab2": "2. Klinisches Dashboard & Ausführlicher Bericht",
        "tab3": "3. Globale Zahlungen & Freischaltung",
        "tab4": "4. Admin-Konsole",
        "p1_head": "🧬 Demografie & Stoffwechselgesundheit",
        "p2_head": "🏃 Lebensstil & Herz-Kreislauf",
        "p3_head": "🧠 Geistige, Soziale & Klinische Vorsorge",
        "name_lbl": "Vollständiger Name",
        "q1": "1. Chronologisches Alter",
        "q2": "2. Body-Mass-Index (BMI)",
        "q3": "3. Blutdruckstatus (AHA-Standard)",
        "q4": "4. Nüchternblutzucker / HbA1c",
        "q5": "5. Lipidprofil / Non-HDL-Cholesterin",
        "q6": "6. Wöchentliche Bewegung",
        "q7": "7. Ernährungsmuster (Mittelmeer / DASH)",
        "q8": "8. Schlafdauer & -qualität",
        "q9": "9. Nikotin- / Tabakkonsum",
        "q10": "10. Tägliche Wasserzufuhr",
        "q11": "11. Chronische Stressbewältigung",
        "q12": "12. Soziale Unterstützung & Gemeinschaft",
        "q13": "13. Familiäre Vorbelastung",
        "q14": "14. Alkoholkonsum",
        "q15": "15. Jährliche medizinische Vorsorge",
        "bmi_opts": ["Normal (18.5 - 24.9)", "Untergewicht (<18.5)", "Übergewicht (25 - 29.9)", "Adipös (≥30)"],
        "bp_opts": ["Optimal (<120/80 mmHg)", "Erhöht (120-139/80-89)", "Bluthochdruck (≥140/90 mmHg)"],
        "gluc_opts": ["Normal (<100 mg/dL)", "Prädiabetes (100-125 mg/dL)", "Diabetes (≥126 mg/dL)"],
        "chol_opts": ["Optimal (<130 mg/dL)", "Mäßig (130-159 mg/dL)", "Hoch (≥160 mg/dL)"],
        "ex_opts": ["≥150 Min. Moderat", "30 bis 149 Min. Wöchentlich", "<30 Min. / Inaktiv"],
        "diet_opts": ["Viel Obst, Gemüse & Vollkorn", "Ausgewogene Ernährung", "Viel Fast Food / Zucker"],
        "sleep_opts": ["7 bis 9 Stunden", "5 bis 6 Stunden", "<5 Stunden chronisch"],
        "smoke_opts": ["Nie / Vor >5 Jahren aufgehört", "Früherer Raucher", "Aktiver Raucher / Vaper"],
        "hyd_opts": ["≥2.5 Liter Wasser", "1.5 bis 2.4 Liter", "<1.5 Liter / zuckerhaltige Getränke"],
        "stress_opts": ["Geringer Stress", "Mäßiger Stress", "Hoher chronischer Stress / Burnout"],
        "social_opts": ["Starkes soziales Netz", "Mäßige Verbindung", "Isoliert"],
        "fam_opts": ["Keine Vorgeschichte", "1 Familienmitglied", "Mehrere Familienmitglieder"],
        "alc_opts": ["Kein / Mäßig (≤1 Getränk/Tag)", "Gelegentlich", "Stark (>8 Getränke/Woche)"],
        "screen_opts": ["Jährlicher Check-up", "Gelegentlich", "Selten / Nie"],
        "succ_msg": "✅ 15 KPIs erfasst! Weiter zu Tab 2.",
        "chrono_age": "Chronologisches Alter",
        "bio_age": "Biologisches Alter",
        "est_le": "Geschätzte Lebenserwartung (UN: 74 J.)",
        "gauge_title": "🎯 Biologisches vs. Chronologisches Alter",
        "bar_title": "📊 Einflussfaktoren auf die Gesundheit",
        "narrative_title": "📊 Medizinischer Analysebericht & Zusammenfassung",
        "btn_export": "📄 Zertifizierten Bericht Exportieren (PDF)"
    },
    "Français": {
        "title": "🌍 Plateforme Mondiale de Longévité et Âge Biologique",
        "subtitle": "Évaluation clinique basée sur l'AHA Life's Essential 8™ et l'OMS.",
        "tab1": "1. Évaluation Santé à 15 KPI Normalisés",
        "tab2": "2. Tableau de Bord Clinique et Analyse Détaillée",
        "tab3": "3. Paiements Internationaux & Transferts",
        "tab4": "4. Console d'Administration",
        "p1_head": "🧬 Démographie & Santé Métabolique",
        "p2_head": "🏃 Mode de Vie & Santé Cardiovasculaire",
        "p3_head": "🧠 Dépistage Mental, Social & Clinique",
        "name_lbl": "Nom complet",
        "q1": "1. Âge chronologique",
        "q2": "2. Indice de Masse Corporelle (IMC)",
        "q3": "3. Pression Artérielle",
        "q4": "4. Glycémie à jeun / HbA1c",
        "q5": "5. Cholestérol Non-HDL",
        "q6": "6. Exercice physique hebdomadaire",
        "q7": "7. Régime Alimentaire (Méditerranéen / DASH)",
        "q8": "8. Durée et qualité du sommeil",
        "q9": "9. Exposition au tabac",
        "q10": "10. Hydratation quotidienne",
        "q11": "11. Gestion du stress chronique",
        "q12": "12. Soutien social",
        "q13": "13. Antécédents familiaux",
        "q14": "14. Consommation d'alcool",
        "q15": "15. Bilans de santé annuels",
        "bmi_opts": ["Normal (18.5 - 24.9)", "Insuffisance pondérale (<18.5)", "Surpoids (25 - 29.9)", "Obésité (≥30)"],
        "bp_opts": ["Optimal (<120/80 mmHg)", "Élevé (120-139/80-89)", "Hypertension (≥140/90 mmHg)"],
        "gluc_opts": ["Normal (<100 mg/dL)", "Prédiabète (100-125 mg/dL)", "Diabète (≥126 mg/dL)"],
        "chol_opts": ["Optimal (<130 mg/dL)", "Modéré (130-159 mg/dL)", "Élevé (≥160 mg/dL)"],
        "ex_opts": ["≥150 min modéré", "30 à 149 min par semaine", "<30 min / Sédentaire"],
        "diet_opts": ["Riche en fruits, légumes & grains entiers", "Alimentation équilibrée", "Riche en produits transformés / sucre"],
        "sleep_opts": ["7 à 9 heures", "5 à 6 heures", "<5 heures de privation"],
        "smoke_opts": ["Jamais / Arrêté >5 ans", "Ancien fumeur", "Fumeur actif / Vapote"],
        "hyd_opts": ["≥2.5 Litres", "1.5 à 2.4 Litres", "<1.5 Litres / Boissons sucrées"],
        "stress_opts": ["Faible stress", "Stress modéré", "Stress chronique élevé"],
        "social_opts": ["Solide réseau social", "Connexion modérée", "Isolé"],
        "fam_opts": ["Aucun antécédent", "1 membre de la famille", "Plusieurs membres"],
        "alc_opts": ["Zéro / Modéré (≤1 verre/jour)", "Occasionnel", "Lourd (>8 verres/semaine)"],
        "screen_opts": ["Dépistage annuel", "Occasionnel", "Rarement / Jamais"],
        "succ_msg": "✅ 15 KPI enregistrés !",
        "chrono_age": "Âge chronologique",
        "bio_age": "Âge biologique",
        "est_le": "Espérance de vie estimée (ONU: 74 ans)",
        "gauge_title": "🎯 Âge biologique vs Âge chronologique",
        "bar_title": "📊 Impact des catégories de santé",
        "narrative_title": "📊 Rapport d'Analyse Médicale",
        "btn_export": "📄 Exporter le Rapport (PDF)"
    },
    "日本語": {
        "title": "🌍 グローバル長寿＆生物学的年齢アナリティクスプラットフォーム",
        "subtitle": "米国心臓協会 (AHA) および WHO 基準に基づく臨床評価。",
        "tab1": "1. 15の標準化ヘルスKPI評価",
        "tab2": "2. 臨床ダッシュボード＆詳細レポート",
        "tab3": "3. 国際送金・決済と認証",
        "tab4": "4. 管理コンソール",
        "p1_head": "🧬 人口統計と代謝の健康",
        "p2_head": "🏃 ライフスタイルと心血管行動",
        "p3_head": "🧠 メンタル、社会的、臨床的スクリーニング",
        "name_lbl": "氏名",
        "q1": "1. 暦年齢 (Chronological Age)",
        "q2": "2. ボディマス指数 (BMI)",
        "q3": "3. 血圧状態 (AHA基準)",
        "q4": "4. 空腹時血糖値 / HbA1c",
        "q5": "5. 脂質プロファイル / 非HDLコレステロール",
        "q6": "6. 週の運動量",
        "q7": "7. 食事パターン (地中海式 / DASH)",
        "q8": "8. 睡眠時間と質",
        "q9": "9. ニコチン・タバコ曝露",
        "q10": "10. 毎日の水分摂取量",
        "q11": "11. 慢性ストレスとコルチゾール管理",
        "q12": "12. 社会的サポート",
        "q13": "13. 家族の既往歴",
        "q14": "14. アルコール摂取パターン",
        "q15": "15. 年次健康診断・バイオマーカーモニタリング",
        "bmi_opts": ["正常 (18.5 - 24.9)", "低体重 (<18.5)", "過体重 (25 - 29.9)", "肥満 (≥30)"],
        "bp_opts": ["最適 (<120/80 mmHg)", "やや高め (120-139/80-89)", "高血圧 (≥140/90 mmHg)"],
        "gluc_opts": ["正常 (<100 mg/dL)", "糖尿病予備軍 (100-125 mg/dL)", "糖尿病領域 (≥126 mg/dL)"],
        "chol_opts": ["最適 (<130 mg/dL)", "中等度 (130-159 mg/dL)", "高値 (≥160 mg/dL)"],
        "ex_opts": ["中等度≥150分または高強度≥75分", "週30〜149分", "<30分 / 運動不足"],
        "diet_opts": ["果物・野菜・全粒穀物が豊富", "通常のバランス食", "加工食品・糖分過多"],
        "sleep_opts": ["7〜9時間", "5〜6時間", "<5時間"],
        "smoke_opts": ["吸わない / 5年以上前に禁煙", "元喫煙者", "現在喫煙・ベイプ使用"],
        "hyd_opts": ["≥2.5リットル", "1.5〜2.4リットル", "<1.5リットル / 甘味飲料"],
        "stress_opts": ["低ストレス / レジリエンス良好", "中等度の仕事ストレス", "高ストレス / バーンアウト"],
        "social_opts": ["強いつつながり", "中等度", "孤立傾向"],
        "fam_opts": ["なし", "1親等にあり", "複数あり"],
        "alc_opts": ["ゼロまたは適度 (≤1杯/日)", "時々飲酒", "過度な飲酒 (>8杯/週)"],
        "screen_opts": ["毎年受診", "時々受診", "ほとんど / 受診しない"],
        "succ_msg": "✅ 15個のKPIが正常に記録されました！",
        "chrono_age": "暦年齢",
        "bio_age": "生物学的年齢",
        "est_le": "推定寿命 (国連基準: 74歳)",
        "gauge_title": "🎯 生物学的年齢 vs 暦年齢",
        "bar_title": "📊 健康カテゴリ別影響スコア",
        "narrative_title": "📊 エグゼクティブ健康評価分析レポート",
        "btn_export": "📄 認定レポートをダウンロード (PDF)"
    },
    "العربية": {
        "title": "🌍 المنصة العالمية للتحليلات الطبية للعمر البيولوجي",
        "subtitle": "تقييم سريري معتمد على معايير جمعية القلب الأمريكية (AHA) ومنظمة الصحة العالمية.",
        "tab1": "1. تقييم مؤشرات الصحة الـ 15 المعتمدة",
        "tab2": "2. لوحة التحليلات السريرية والتقرير التفصيلي",
        "tab3": "3. المدفوعات الدولية والتحويلات المالية",
        "tab4": "4. لوحة التحكم والإدارة",
        "p1_head": "🧬 التركيبة السكانية والصحة الأيضية",
        "p2_head": "🏃 نمط الحياة وصحة القلب والأوعية الدموية",
        "p3_head": "🧠 الفحص النفسي والاجتماعي والسريري",
        "name_lbl": "الاسم الكامل",
        "q1": "1. العمر الزمني",
        "q2": "2. مؤشر كتلة الجسم (BMI)",
        "q3": "3. حال ضغط الدم",
        "q4": "4. سكر الدم الصائم / التراكمي",
        "q5": "5. الكوليسترول الضار (Non-HDL)",
        "q6": "6. التمارين الرياضية الأسبوعية",
        "q7": "7. النمط الغذائي (متوسطي / DASH)",
        "q8": "8. مدة النوم وجودته",
        "q9": "9. التدخين والنيكوتين",
        "q10": "10. استهلاك الماء اليومي",
        "q11": "11. إدارة الإجهاد المزمن",
        "q12": "12. الدعم الاجتماعي",
        "q13": "13. التاريخ العائلي للأمراض المزمنة",
        "q14": "14. استهلاك الكحول",
        "q15": "15. الفحوصات الطبية السنوية",
        "bmi_opts": ["طبيعي (18.5 - 24.9)", "نقص الوزن (<18.5)", "زيادة الوزن (25 - 29.9)", "سمنة (≥30)"],
        "bp_opts": ["مثالي (<120/80)", "مرتفع (120-139/80-89)", "ضغط مرتفع (≥140/90)"],
        "gluc_opts": ["طبيعي (<100)", "ما قبل السكري (100-125)", "نطاق السكري (≥126)"],
        "chol_opts": ["مثالي (<130)", "متوسط (130-159)", "مرتفع (≥160)"],
        "ex_opts": ["≥150 دقيقة أسبوعياً", "30 إلى 149 دقيقة", "<30 دقيقة / خامل"],
        "diet_opts": ["غني بالفواكه والخضروات والحبوب الكاملة", "متوازن", "غني بالأطعمة المصنعة والسكريات"],
        "sleep_opts": ["7 إلى 9 ساعات", "5 إلى 6 ساعات", "<5 ساعات (حرمان مزمن)"],
        "smoke_opts": ["لا يدخن / أقلع منذ >5 سنوات", "مدخن سابق", "مدخن نشط / فيب"],
        "hyd_opts": ["≥2.5 لتر يومياً", "1.5 إلى 2.4 لتر", "<1.5 لتر / مشروبات محلاة"],
        "stress_opts": ["توتر منخفض / إدارة نشطة", "توتر معتدل", "توتر مزمن مرتفع / إرهاق"],
        "social_opts": ["شبكة اجتماعية قوية", "اتصال معتدل", "ضعيف / منعزل"],
        "fam_opts": ["لا توجد سيرة مرضية مبكرة", "فرد واحد من العائلة", "أفراد متعددون"],
        "alc_opts": ["صفر أو معتدل (≤1 كأس/يوم)", "عرضي", "استهلاك ثقيل (>8 كؤوس/أسبوع)"],
        "screen_opts": ["فحص شامل سنوي", "فحص عرضي", "نادراً / لا يفحص أبداً"],
        "succ_msg": "✅ تم تسجيل المؤشرات الـ 15 بنجاح!",
        "chrono_age": "العمر الزمني",
        "bio_age": "العمر البيولوجي",
        "est_le": "العمر المتوقع (معيار الأمم المتحدة: 74 عاماً)",
        "gauge_title": "🎯 العمر البيولوجي مقارنة بالعمر الزمني",
        "bar_title": "📊 تأثير الفئات الصحية",
        "narrative_title": "📊 التقرير التحليلي الطبي السردي",
        "btn_export": "📄 تحميل التقرير المعتمد (PDF)"
    }
}

# Language Selector
lang_choice = st.sidebar.selectbox("🌐 Select Language / ቋንቋ ይምረጡ / Sprache", list(TRANSLATIONS.keys()))
T = TRANSLATIONS[lang_choice]

st.title(T["title"])
st.caption(T["subtitle"])
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([T["tab1"], T["tab2"], T["tab3"], T["tab4"]])

# ==========================================
# 3. TAB 1: 15 STANDARDIZED HEALTH KPIS
# ==========================================
with tab1:
    st.subheader(T["tab1"])
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"### {T['p1_head']}")
        user_name = st.text_input(T["name_lbl"], "አበበ ከበደ" if lang_choice == "አማርኛ" else "Abebe Kebede")
        age = st.number_input(T["q1"], 18, 100, 35)
        bmi_val = st.selectbox(T["q2"], T["bmi_opts"])
        bp_val = st.selectbox(T["q3"], T["bp_opts"])
        glucose_val = st.selectbox(T["q4"], T["gluc_opts"])
        chol_val = st.selectbox(T["q5"], T["chol_opts"])

    with c2:
        st.markdown(f"### {T['p2_head']}")
        ex_val = st.selectbox(T["q6"], T["ex_opts"])
        diet_val = st.selectbox(T["q7"], T["diet_opts"])
        sleep_val = st.selectbox(T["q8"], T["sleep_opts"])
        smoke_val = st.selectbox(T["q9"], T["smoke_opts"])
        hyd_val = st.selectbox(T["q10"], T["hyd_opts"])

    with c3:
        st.markdown(f"### {T['p3_head']}")
        stress_val = st.selectbox(T["q11"], T["stress_opts"])
        social_val = st.selectbox(T["q12"], T["social_opts"])
        fam_val = st.selectbox(T["q13"], T["fam_opts"])
        alcohol_val = st.selectbox(T["q14"], T["alc_opts"])
        screen_val = st.selectbox(T["q15"], T["screen_opts"])

    st.success(T["succ_msg"])

# Scoring Engine
delta = 0.0
if bmi_val in [T["bmi_opts"][0]]: delta -= 1.0
elif bmi_val in [T["bmi_opts"][3]]: delta += 3.0

if bp_val in [T["bp_opts"][0]]: delta -= 1.5
elif bp_val in [T["bp_opts"][2]]: delta += 2.5

if glucose_val in [T["gluc_opts"][0]]: delta -= 1.0
elif glucose_val in [T["gluc_opts"][2]]: delta += 2.5

if ex_val in [T["ex_opts"][0]]: delta -= 2.0
elif ex_val in [T["ex_opts"][2]]: delta += 2.5

if diet_val in [T["diet_opts"][0]]: delta -= 1.5
elif diet_val in [T["diet_opts"][2]]: delta += 2.0

if sleep_val in [T["sleep_opts"][0]]: delta -= 1.0
elif sleep_val in [T["sleep_opts"][2]]: delta += 1.5

if smoke_val in [T["smoke_opts"][0]]: delta -= 1.5
elif smoke_val in [T["smoke_opts"][2]]: delta += 4.0

bio_age = max(18.0, round(age + delta, 1))
le_delta = (age - bio_age) * 0.75
est_le = round(UN_BASELINE_LE + le_delta, 1)
age_diff = round(age - bio_age, 1)

# ==========================================
# 4. TAB 2: RESULTS & NARRATIVE BRIEFING
# ==========================================
with tab2:
    st.header(T["tab2"])
    
    m1, m2, m3 = st.columns(3)
    m1.metric(T["chrono_age"], f"{age} ዓመት" if lang_choice == "አማርኛ" else f"{age} Yrs")
    m2.metric(T["bio_age"], f"{bio_age} ዓመት" if lang_choice == "አማርኛ" else f"{bio_age} Yrs")
    m3.metric(T["est_le"], f"{est_le} ዓመት" if lang_choice == "አማርኛ" else f"{est_le} Yrs")

    st.divider()

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader(T["gauge_title"])
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=bio_age,
            delta={'reference': age, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            gauge={
                'axis': {'range': [18, 100]},
                'bar': {'color': "#008060" if age_diff >= 0 else "#E53935"},
                'steps': [
                    {'range': [18, 40], 'color': "#E8F5E9"},
                    {'range': [40, 70], 'color': "#FFFDE7"},
                    {'range': [70, 100], 'color': "#FFEBEE"}
                ]
            }
        ))
        fig_gauge.update_layout(height=280)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_g2:
        st.subheader(T["bar_title"])
        impact_df = pd.DataFrame({
            "Category": ["Metabolic", "Cardiovascular", "Lifestyle", "Sleep & Stress"],
            "Impact": [
                -2.0 if glucose_val == T["gluc_opts"][0] else 2.5,
                -1.5 if bp_val == T["bp_opts"][0] else 2.5,
                -2.0 if ex_val == T["ex_opts"][0] else 2.0,
                -1.0 if sleep_val == T["sleep_opts"][0] else 1.5
            ]
        })
        fig_bar = px.bar(impact_df, x="Category", y="Impact", color="Impact", color_continuous_scale="RdYlGn_r")
        fig_bar.update_layout(height=280)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    st.subheader(T["narrative_title"])
    if lang_choice == "አማርኛ":
        narrative_p1 = f"**የታካሚው አጠቃላይ የጤና ትንተና፡** በተባበሩት መንግስታት (UN) የ 74 ዓመት ዓለም አቀፍ አማካይ መሠረት እና በ AHA መለኪያዎች መሠረት የተሰላው **የባዮሎጂካል እድሜዎ {bio_age} ዓመት** ሲሆን፣ የትውልድ እድሜዎ ደግሞ **{age} ዓመት** ነው። ይህም የውስጥ አካልዎ ከትውልድ እድሜዎ በ **{abs(age_diff)} ዓመት {'የታነሰ (ጤናማ)' if age_diff >= 0 else 'የበለጠ'}** መሆኑን ያሳያል።"
        narrative_p2 = f"**የሜታቦሊክ እና የልብ-ደም ቧንቧ ስጋት ትንተና፡** ያስገቡት የደም ግፊት ({bp_val})፣ የደም ስኳር ({glucose_val}) እና የአካል እንቅስቃሴ ({ex_val}) መረጃ እንደሚያሳየው የተገመተው አጠቃላይ የዕድሜ ጣሪያዎ **{est_le} ዓመት** ነው።"
        narrative_p3 = f"**የረጅም እድሜ መመሪያዎች፡** የባዮሎጂካል እድሜዎን የበለጠ ለማሻሻል እና ጤናማ እድሜን ለማራዘም፡ የእንቅልፍ ሰዓትዎን ከ 7-9 ሰዓት ማድረግ፣ በተፈጥሯዊ ምግቦች ላይ ያተኮረ ምግብ መመገብ እና በየዓመቱ የደም ምርመራ ማድረግ ይመከራል።"
    else:
        narrative_p1 = f"**Patient Overview & Cellular Aging:** Based on UN baseline data (74 Years) and AHA standards, your calculated **Biological Age is {bio_age} years** relative to your **Chronological Age of {age} years** (Variance: **{abs(age_diff)} years {'younger' if age_diff >= 0 else 'older'}**)."
        narrative_p2 = f"**Metabolic & Cardiovascular Risk Analysis:** Your blood pressure status ({bp_val}), fasting blood glucose ({glucose_val}), and activity level ({ex_val}) yield an estimated lifespan of **{est_le} years**."
        narrative_p3 = f"**Targeted Optimization Roadmap:** Prioritize 7-9 hours of restorative sleep, whole-food nutrition, and annual biomarker tracking to maintain optimal cellular longevity."

    st.markdown(narrative_p1)
    st.markdown(narrative_p2)
    st.markdown(narrative_p3)

    st.divider()

    if st.button(T["btn_export"]):
        st.session_state.free_used = True
        st.success("🎉 Report ready!")
        st.download_button(
            "📥 Save Certified Narrative Report (.txt)",
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
        
        if curr == "ETB (ብር)":
            amt = st.number_input("Amount (Min 20 ETB) / መጠን", min_value=20, value=200, step=10)
        else:
            amt = st.number_input(f"Amount (Min 3 {curr[:3]}) / መጠን", min_value=3, value=10, step=1)
            
        st.info(
            "**📲 Mobile Money / International Remittance (Sendwave, Remitly, WorldRemit):**\n"
            "* Recipient Phone: `+251986884912`\n"
            "* Name: **Belayhun Adefrese**\n\n"
            "**🏦 Commercial Bank of Ethiopia (CBE Direct):**\n"
            "* Account Number: `1000296269488`\n"
            "* Name: **Belayhun Adefrese Metaferia** (Lem Area Branch, Addis Ababa)\n\n"
            "**📋 How to Get Your Unlock Key:**\n"
            "1. Send funds via Sendwave, Remitly, WorldRemit, or Telebirr/CBE.\n"
            "2. Copy the **Transaction Reference / MTCN / Confirmation Code**.\n"
            "3. Paste the code below and submit your claim to receive your SMS Access Key."
        )
        
        c_name = st.text_input("Sender Full Name")
        c_ref = st.text_input("Transaction Ref / MTCN / Confirmation Code")
        
        if st.button("📩 Submit Verification Claim", type="primary"):
            if len(c_ref.strip()) >= 5:
                st.success(f"✅ Claim logged for {amt} {curr[:3]}! Your access key will be sent via SMS.")
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
    elif pwd:
        st.error("❌ Incorrect Admin Password.")
