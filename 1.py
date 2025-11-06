import streamlit as st
import pandas as pd
import random

# ---------------- Page Config ----------------
st.set_page_config(page_title="Harshithaa | AI Portfolio", page_icon="🎤", layout="wide")

# ---------------- Sidebar Navigation ----------------
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Dashboard", "👩‍💻 About Me", "🚀 Projects", "📫 Contact"])

# ---------------- PAGE 1: DASHBOARD ----------------
if page == "🏠 Dashboard":
    st.title("🎤 AI Interview Coach Dashboard")
    st.caption("Analyze interview responses and get AI-powered insights")

    # Load dataset
    df = pd.read_csv("NewApp.csv", sep=None, engine="python")
    df.columns = df.columns.str.strip().str.lower()

    if 'question_category' not in df.columns:
        st.error("⚠️ 'question_category' column not found! Please recheck your CSV header.")
        st.stop()

    category = st.sidebar.selectbox(
        "Select Question Category",
        sorted(df["question_category"].dropna().unique().tolist())
    )
    filtered = df[df["question_category"] == category]

    # Helper functions
    def performance_badge(conf):
        if conf >= 8:
            return "🟢 Excellent"
        elif conf >= 5:
            return "🟡 Moderate"
        else:
            return "🔴 Needs Practice"

    def color_confidence(val):
        if val >= 8:
            return "background-color:#00C853; color:white; font-weight:bold; border-radius:4px;"
        elif val >= 5:
            return "background-color:#FFD600; color:black; font-weight:bold; border-radius:4px;"
        else:
            return "background-color:#D50000; color:white; font-weight:bold; border-radius:4px;"

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Responses", len(df))
    col2.metric("Categories", df["question_category"].nunique())
    col3.metric("Avg Confidence", round(df["confidence_score"].mean(), 2))
    col4.metric("Avg Clarity", round(df["clarity_score"].mean(), 2))
    st.divider()

    # Category analysis
    st.subheader(f"🗂 Responses for: {category}")
    avg_conf = round(filtered["confidence_score"].mean(), 2)
    badge = performance_badge(avg_conf)
    st.markdown(f"### Overall Performance: {badge}")

    styled = filtered[
        ["user_response_text","confidence_score","clarity_score","tone","sentiment_label","improvement_tips"]
    ].style.applymap(color_confidence, subset=["confidence_score"])
    st.dataframe(styled, use_container_width=True)

    # Charts
    st.subheader("📈 Average Scores by Category")
    avg_data = df.groupby("question_category")[["confidence_score","clarity_score"]].mean().sort_values("confidence_score", ascending=False)
    st.bar_chart(avg_data)

    st.subheader("📊 Confidence vs Clarity Trend")
    trend_data = df.groupby("question_category")[["confidence_score","clarity_score"]].mean()
    st.line_chart(trend_data)

    # AI Feedback
    st.divider()
    st.subheader("🤖 AI Feedback Summary")

    def ai_feedback(avg_conf, avg_clarity, tone):
        feedback_templates = [
            f"Your answers show **strong confidence ({avg_conf}/10)** and balanced clarity ({avg_clarity}/10). Keep that up in {category}!",
            f"You have steady confidence and clarity at {avg_clarity}/10. Try simplifying your responses in {category} for more impact.",
            f"Good effort! With clarity at {avg_clarity}, focus on adding examples to strengthen {category} answers.",
            f"Tone ({tone}) reflects professionalism — maintain assertiveness and calm in {category} situations."
        ]
        return random.choice(feedback_templates)

    avg_clarity = round(filtered["clarity_score"].mean(), 2)
    tone_mode = filtered["tone"].mode()[0] if not filtered.empty else "Neutral"
    feedback = ai_feedback(avg_conf, avg_clarity, tone_mode)
    st.info(feedback)

    # Download
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download This Category Data",
        data=csv,
        file_name=f"{category}_responses.csv",
        mime="text/csv",
    )

# ---------------- PAGE 2: ABOUT ME ----------------
elif page == "👩‍💻 About Me":
    st.title("👩‍💻 About Me")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
    st.markdown("""
    Hi! I'm **Harshithaa**, an AI/ML student passionate about intelligent systems and real-world data applications.  
    I love building meaningful projects that combine **data, design, and AI** to solve problems.

    ### 🎓 Education
    - B.Tech in Artificial Intelligence  
    - 5th Semester, AI Major  

    ### 🧠 Skills
    - Python, Java, Pandas, Streamlit  
    - Machine Learning, Data Visualization  
    - UI Design, Communication & Leadership  
    """)

# ---------------- PAGE 3: PROJECTS ----------------
elif page == "🚀 Projects":
    st.title("🚀 My Projects")
    st.markdown("""
    ### 🎤 AI Interview Coach Dashboard
    - Interactive analysis of interview responses  
    - Generates AI feedback & performance badges  

    ### 🧭 AI Career Path Recommender
    - Recommends tech roles using skill-based mapping  

    ### 💳 Cheque Fraud Detection
    - CNN-based model detecting fraudulent cheque images  

    ### 🚑 Drone Emergency Delivery System
    - Smart route optimization for emergency deliveries  
    """)

# ---------------- PAGE 4: CONTACT ----------------
elif page == "📫 Contact":
    st.title("📫 Contact Me")
    st.markdown("""
    💼 **LinkedIn:** [linkedin.com/in/harshithaa](https://linkedin.com)  
    💻 **GitHub:** [github.com/harshithaamn](https://github.com/harshithaamn)  
    ✉️ **Email:** harshithaa@example.com  
    📍 Based in: India 🇮🇳  
    """)
