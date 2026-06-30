import streamlit as st
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="SEO Content Intelligence",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------
# THEME TOGGLE (DARK / LIGHT)
# -----------------------------
theme = st.sidebar.toggle("🌙 Dark Mode", value=True)

if theme:
    st.markdown(
        """
        <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# TITLE
# -----------------------------
st.title("🚀 SEO Content Refresh Intelligence Tool")
st.caption("Upload Google Search Console CSV to get SEO optimization insights")

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
        actions.append("Improve Title & Meta Description (CTR issue)")

    if impressions > 1000 and clicks < 50:
        score += 30
        actions.append("Rewrite title to increase clicks")

    if position > 10:
        score += 20
        actions.append("Improve content depth + internal linking")

    if clicks < 10:
        score += 10
        actions.append("Expand content + add FAQs section")

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

    st.success("File uploaded successfully ✔")

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
    # FILTERS
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        priority_filter = st.selectbox(
            "Filter by Priority",
            ["ALL", "HIGH 🔴", "MEDIUM 🟠", "LOW 🟢"]
        )

    if priority_filter != "ALL":
        result_df = result_df[result_df["Priority"] == priority_filter]

    # -----------------------------
    # EXPANDABLE UI (NO TEXT CUTTING)
    # -----------------------------
    st.subheader("📊 Content Refresh Recommendations")

    for _, row in result_df.iterrows():

        with st.expander(f"{row['Priority']} | {row['Page']}"):

            st.write("### SEO Metrics")
            st.write("Clicks:", row["Clicks"])
            st.write("Impressions:", row["Impressions"])
            st.write("CTR:", row["CTR"])
            st.write("Position:", row["Position"])

            st.write("### Recommendations")
            st.write(row["Recommendations"])

    # -----------------------------
    # DOWNLOAD REPORT
    # -----------------------------
    st.download_button(
        "📥 Download SEO Report",
        result_df.to_csv(index=False),
        "seo_content_refresh_report.csv",
        mime="text/csv"
    )
