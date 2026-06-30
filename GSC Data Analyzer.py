import streamlit as st
import pandas as pd

st.title("🚀 GSC Content Refresh Analyzer")

st.write("Upload Google Search Console CSV export")

file = st.file_uploader("Upload CSV", type=["csv"])


# -----------------------------
# Analysis Logic
# -----------------------------
def analyze(row):

    clicks = row["Clicks"]
    impressions = row["Impressions"]
    ctr = row["CTR"]
    position = row["Position"]

    score = 0
    actions = []

    # High impressions but low CTR
    if impressions > 1000 and ctr < 2:
        score += 40
        actions.append("Improve Title & Meta Description (CTR issue)")

    # High impressions but low clicks
    if impressions > 1000 and clicks < 50:
        score += 30
        actions.append("Content not attracting clicks → rewrite snippet")

    # Bad position
    if position > 10:
        score += 20
        actions.append("Improve SEO content depth + internal linking")

    # Low performance page
    if clicks < 10:
        score += 10
        actions.append("Add FAQs + expand content")

    # Priority
    if score >= 60:
        priority = "HIGH 🔴"
    elif score >= 30:
        priority = "MEDIUM 🟠"
    else:
        priority = "LOW 🟢"

    return priority, actions


# -----------------------------
# MAIN
# -----------------------------
if file:

    df = pd.read_csv(file)

    st.write("### Raw Data Preview")
    st.dataframe(df)

    results = []

    for _, row in df.iterrows():

        priority, actions = analyze(row)

        results.append({
            "Page": row["Page"],
            "Clicks": row["Clicks"],
            "Impressions": row["Impressions"],
            "CTR": row["CTR"],
            "Position": row["Position"],
            "Priority": priority,
            "Recommendations": " | ".join(actions)
        })

    result_df = pd.DataFrame(results)

    st.write("### 🚀 Content Refresh Recommendations")
    st.dataframe(result_df)

    st.download_button(
        "Download Report",
        result_df.to_csv(index=False),
        "gsc_report.csv"
    )