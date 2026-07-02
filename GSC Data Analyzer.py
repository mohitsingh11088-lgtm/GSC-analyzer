import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="SEO Content Intelligence (Free)", layout="wide")

st.title("🚀 SEO Content Intelligence Dashboard (FREE VERSION)")
st.caption("No API | Rule-based SEO analysis for GSC data")

# -----------------------------
# CLEAN FUNCTION
# -----------------------------
def clean_number(v):
    try:
        if pd.isna(v):
            return 0
        return float(str(v).replace("%", "").strip())
    except:
        return 0


# -----------------------------
# SEO SCORE ENGINE
# -----------------------------
def seo_score(clicks, impressions, ctr, position):

    score = 100
    actions = []

    # LOW CTR ISSUE
    if impressions > 1000 and ctr < 2:
        score -= 25
        actions.append("Improve title & meta description to increase CTR")

    # LOW POSITION ISSUE
    if position > 15:
        score -= 30
        actions.append("Improve content depth + internal linking")

    # LOW CLICKS ISSUE
    if clicks < 20 and impressions > 500:
        score -= 20
        actions.append("Optimize content for user intent")

    # VERY LOW PERFORMANCE
    if clicks < 10:
        score -= 15
        actions.append("Add FAQs + expand content coverage")

    # FINAL LABEL
    if score >= 80:
        priority = "LOW 🟢"
    elif score >= 50:
        priority = "MEDIUM 🟠"
    else:
        priority = "HIGH 🔴"

    return score, priority, actions


# -----------------------------
# QUERY INSIGHT ENGINE (FREE)
# -----------------------------
def query_insights(query, ctr, position):

    tips = []

    if ctr < 2:
        tips.append(f"Improve CTR for query: '{query}'")

    if position > 10:
        tips.append(f"Create dedicated section targeting '{query}'")

    if not tips:
        tips.append("Query is performing well")

    return " | ".join(tips)


# -----------------------------
# UPLOAD FILE
# -----------------------------
file = st.file_uploader("Upload GSC CSV", type=["csv"])

if file:

    df = pd.read_csv(file)
    df = df.head(50)

    st.subheader("📄 Raw Data Preview")
    st.dataframe(df, use_container_width=True)

    results = []

    mode = st.selectbox("Choose Analysis Mode", ["Pages", "Queries"])

    for row in df.itertuples():

        clicks = clean_number(getattr(row, "Clicks", 0))
        impressions = clean_number(getattr(row, "Impressions", 0))
        ctr = clean_number(getattr(row, "CTR", 0))
        position = clean_number(getattr(row, "Position", 0))

        name = getattr(row, "Top_pages", None) or getattr(row, "Query", None) or "Unknown"

        if mode == "Pages":

            score, priority, actions = seo_score(clicks, impressions, ctr, position)

            results.append({
                "Page": name,
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "SEO Score": score,
                "Priority": priority,
                "Recommendations": " | ".join(actions)
            })

        else:

            insight = query_insights(name, ctr, position)

            results.append({
                "Query": name,
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Insights": insight
            })

    result_df = pd.DataFrame(results)

    st.subheader("📊 SEO Analysis Results")
    st.dataframe(result_df, use_container_width=True)

    st.download_button(
        "📥 Download Report",
        result_df.to_csv(index=False),
        "seo_report.csv",
        mime="text/csv"
    )
