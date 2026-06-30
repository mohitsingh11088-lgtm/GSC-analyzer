import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Content Gap AI System",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Content Gap AI System (GSC Powered)")
st.caption("Find missing content opportunities from Search Console data")

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
# SIMPLE TOPIC CLUSTERING
# -----------------------------
def get_topic(query):

    q = query.lower()

    if any(x in q for x in ["seo", "ranking", "google"]):
        return "SEO"
    elif any(x in q for x in ["ads", "ppc", "google ads"]):
        return "Paid Ads"
    elif any(x in q for x in ["content", "blog", "writing"]):
        return "Content Marketing"
    elif any(x in q for x in ["social", "instagram", "facebook"]):
        return "Social Media"
    elif any(x in q for x in ["tools", "software", "crm"]):
        return "Tools / Software"
    elif any(x in q for x in ["how", "what", "why", "guide"]):
        return "Educational / How-to"
    else:
        return "General"


# -----------------------------
# BLOG IDEA GENERATOR
# -----------------------------
def blog_idea(topic, query):
    return f"Complete Guide to {query} in 2026 ({topic})"


# -----------------------------
# GAP DETECTION
# -----------------------------
def find_gap(impressions, ctr, position):

    gaps = []

    if impressions > 500 and ctr < 2:
        gaps.append("Low CTR → improve title/meta")

    if impressions > 500 and position > 10:
        gaps.append("Ranking gap → create better content page")

    if impressions > 100 and ctr < 1:
        gaps.append("High demand but weak visibility")

    if not gaps:
        gaps.append("No major gap")

    return " | ".join(gaps)


# -----------------------------
# MAIN
# -----------------------------
if file:

    df = pd.read_csv(file)

    st.success("File uploaded successfully ✔")

    st.write("### 📄 Data Preview")
    st.dataframe(df)

    results = []

    for _, row in df.iterrows():

        query = row.get("Query") or row.get("Top queries") or "Unknown Query"

        clicks = clean_number(row.get("Clicks", 0))
        impressions = clean_number(row.get("Impressions", 0))
        ctr = clean_number(row.get("CTR", 0))
        position = clean_number(row.get("Position", 0))

        topic = get_topic(query)

        gap = find_gap(impressions, ctr, position)

        results.append({
            "Query": query,
            "Topic Cluster": topic,
            "Clicks": clicks,
            "Impressions": impressions,
            "CTR": ctr,
            "Position": position,
            "Content Gap": gap,
            "Blog Idea": blog_idea(topic, query)
        })

    result_df = pd.DataFrame(results)

    # -----------------------------
    # FILTERS
    # -----------------------------
    st.subheader("📊 Content Gap Opportunities")

    col1, col2 = st.columns(2)

    with col1:
        topic_filter = st.selectbox(
            "Filter by Topic",
            ["ALL"] + sorted(result_df["Topic Cluster"].unique())
        )

    if topic_filter != "ALL":
        result_df = result_df[result_df["Topic Cluster"] == topic_filter]

    # -----------------------------
    # TABLE VIEW
    # -----------------------------
    st.dataframe(result_df, use_container_width=True)

    # -----------------------------
    # DOWNLOAD
    # -----------------------------
    st.download_button(
        "📥 Download Content Gap Report",
        result_df.to_csv(index=False),
        "content_gap_ai_report.csv",
        mime="text/csv"
    )
