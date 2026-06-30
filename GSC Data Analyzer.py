import streamlit as st
import pandas as pd

st.title("🚀 GSC Content Refresh Analyzer (Final Stable Version)")

st.write("Upload your Google Search Console CSV export")


file = st.file_uploader("Upload CSV", type=["csv"])


# -----------------------------
# CLEANING FUNCTION
# -----------------------------
def clean_number(value):
    try:
        if pd.isna(value):
            return 0

        if isinstance(value, str):
            value = value.replace("%", "").strip()

            if value in ["", "—", "-", "null", "None"]:
                return 0

        return float(value)

    except:
        return 0


# -----------------------------
# ANALYSIS ENGINE
# -----------------------------
def analyze(row):

    clicks = clean_number(row.get("Clicks", 0))
    impressions = clean_number(row.get("Impressions", 0))
    ctr = clean_number(row.get("CTR", 0))
    position = clean_number(row.get("Position", 0))

    score = 0
    actions = []

    # 🔴 CTR issue
    if impressions > 1000 and ctr < 2:
        score += 40
        actions.append("Improve Title & Meta Description (Low CTR)")

    # 🔴 Low clicks despite impressions
    if impressions > 1000 and clicks < 50:
        score += 30
        actions.append("Rewrite title to improve click-through rate")

    # 🔴 Ranking issue
    if position > 10:
        score += 20
        actions.append("Improve content depth + internal linking")

    # 🔴 Weak traffic page
    if clicks < 10:
        score += 10
        actions.append("Expand content + add FAQs section")

    # Priority logic
    if score >= 60:
        priority = "HIGH 🔴"
    elif score >= 30:
        priority = "MEDIUM 🟠"
    else:
        priority = "LOW 🟢"

    return priority, actions


# -----------------------------
# MAIN APP
# -----------------------------
if file:

    df = pd.read_csv(file)

    st.write("### 📄 Raw Data Preview")
    st.dataframe(df)

    st.write("### 📌 Detected Columns")
    st.write(list(df.columns))

    results = []

    for _, row in df.iterrows():

        priority, actions = analyze(row)

        # -----------------------------
        # FIXED PAGE COLUMN LOGIC
        # -----------------------------
        page = (
            row.get("Top pages")
            or row.get("Page")
            or row.get("Landing Page")
            or row.get("URL")
            or "Unknown Page"
        )

        results.append({
            "Page": page,
            "Clicks": clean_number(row.get("Clicks", 0)),
            "Impressions": clean_number(row.get("Impressions", 0)),
            "CTR": clean_number(row.get("CTR", 0)),
            "Position": clean_number(row.get("Position", 0)),
            "Priority": priority,
            "Recommendations": " | ".join(actions) if actions else "No action needed"
        })

    result_df = pd.DataFrame(results)

    st.write("### 🚀 Content Refresh Recommendations")
    st.dataframe(result_df)

    st.download_button(
        label="📥 Download Report",
        data=result_df.to_csv(index=False),
        file_name="gsc_content_refresh_report.csv",
        mime="text/csv"
    )
