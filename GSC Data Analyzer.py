import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SEO Content Intelligence",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 SEO Content Refresh Intelligence Tool")
st.caption("Upload Google Search Console CSV to find optimization opportunities")


file = st.file_uploader("Upload GSC CSV", type=["csv"])


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

    if impressions > 1000 and ctr < 2:
        score += 40
        actions.append("Improve Title & Meta Description")

    if impressions > 1000 and clicks < 50:
        score += 30
        actions.append("Improve CTR with better headline")

    if position > 10:
        score += 20
        actions.append("Improve content depth + internal linking")

    if clicks < 10:
        score += 10
        actions.append("Expand content + add FAQs")

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

    # -----------------------------
    # CLEAN UI HEADER
    # -----------------------------
    st.success("File uploaded successfully ✔")

    # -----------------------------
    # RESULTS PROCESSING
    # -----------------------------
    results = []

    for _, row in df.iterrows():

        priority, actions = analyze(row)

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

    # -----------------------------
    # FILTERS (NEW UX)
    # -----------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["ALL", "HIGH 🔴", "MEDIUM 🟠", "LOW 🟢"]
        )

    if priority_filter != "ALL":
        result_df = result_df[result_df["Priority"] == priority_filter]

    # -----------------------------
    # TABLE OUTPUT (CLEAN)
    # -----------------------------
    st.subheader("📊 Content Refresh Recommendations")

    st.dataframe(
        result_df,
        use_container_width=True
    )

    # -----------------------------
    # DOWNLOAD BUTTON
    # -----------------------------
    st.download_button(
        "📥 Download SEO Report",
        result_df.to_csv(index=False),
        "seo_content_refresh_report.csv",
        mime="text/csv"
    )
