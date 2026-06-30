import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SEO Content Intelligence",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 SEO Content Intelligence Dashboard")
st.caption("Analyze GSC Pages + Queries for content refresh opportunities")

file = st.file_uploader("Upload GSC CSV", type=["csv"])


# -----------------------------
# CLEAN FUNCTION
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
# PAGE ANALYSIS
# -----------------------------
def page_analysis(clicks, impressions, ctr, position):

    score = 0
    actions = []

    if impressions > 1000 and ctr < 2:
        score += 40
        actions.append("Improve Title & Meta Description")

    if impressions > 1000 and clicks < 50:
        score += 30
        actions.append("Improve CTR (rewrite title)")

    if position > 10:
        score += 20
        actions.append("Improve content depth + internal linking")

    if clicks < 10:
        score += 10
        actions.append("Expand content + FAQs")

    if score >= 60:
        priority = "HIGH 🔴"
    elif score >= 30:
        priority = "MEDIUM 🟠"
    else:
        priority = "LOW 🟢"

    return priority, actions


# -----------------------------
# QUERY ANALYSIS (NEW)
# -----------------------------
def query_analysis(query, clicks, impressions, ctr, position):

    suggestions = []

    if impressions > 500 and ctr < 2:
        suggestions.append("Improve title targeting this query")

    if position > 10:
        suggestions.append(f"Create dedicated section for: '{query}'")

    if clicks < 5 and impressions > 100:
        suggestions.append(f"Content mismatch — align content with '{query}' intent")

    if not suggestions:
        suggestions.append("No major issue")

    return " | ".join(suggestions)


# -----------------------------
# MAIN
# -----------------------------
if file:

    df = pd.read_csv(file)

    st.success("File uploaded successfully ✔")

    st.write("### 📄 Raw Data Preview")
    st.dataframe(df)

    # -----------------------------
    # MODE DETECTION
    # -----------------------------
    mode = st.selectbox("Choose Analysis Mode", ["Pages", "Queries"])

    results = []

    # -----------------------------
    # PAGE MODE
    # -----------------------------
    if mode == "Pages":

        for _, row in df.iterrows():

            clicks = clean_number(row.get("Clicks", 0))
            impressions = clean_number(row.get("Impressions", 0))
            ctr = clean_number(row.get("CTR", 0))
            position = clean_number(row.get("Position", 0))

            priority, actions = page_analysis(clicks, impressions, ctr, position)

            page = (
                row.get("Top pages")
                or row.get("Page")
                or row.get("Landing Page")
                or row.get("URL")
                or "Unknown Page"
            )

            results.append({
                "Page": page,
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Priority": priority,
                "Recommendations": " | ".join(actions)
            })

    # -----------------------------
    # QUERY MODE (NEW)
    # -----------------------------
    else:

        for _, row in df.iterrows():

            query = row.get("Query") or row.get("Top queries") or "Unknown Query"

            clicks = clean_number(row.get("Clicks", 0))
            impressions = clean_number(row.get("Impressions", 0))
            ctr = clean_number(row.get("CTR", 0))
            position = clean_number(row.get("Position", 0))

            suggestion = query_analysis(query, clicks, impressions, ctr, position)

            results.append({
                "Query": query,
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Suggestions": suggestion
            })

    result_df = pd.DataFrame(results)

    # -----------------------------
    # FILTER
    # -----------------------------
    st.subheader("📊 Results")

    st.dataframe(result_df, use_container_width=True)

    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    st.download_button(
        "📥 Download Report",
        result_df.to_csv(index=False),
        "seo_insights_report.csv",
        mime="text/csv"
    )
