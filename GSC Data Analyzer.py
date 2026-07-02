import streamlit as st
import pandas as pd
from groq import Groq

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI SEO Intelligence", layout="wide")

st.title("🚀 AI SEO Content Intelligence (Groq Powered)")
st.caption("Hybrid SEO Engine: Rules + AI Insights")

# -----------------------------
# GROQ CLIENT (USE SECRETS IN PRODUCTION)
# -----------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "PASTE_YOUR_KEY_HERE")

client = Groq(api_key=GROQ_API_KEY)

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
# RULE ENGINE (FAST FILTER)
# -----------------------------
def rule_engine(clicks, impressions, ctr, position):
    flags = []

    if position > 15:
        flags.append("ranking_issue")

    if position <= 10 and ctr < 2:
        flags.append("ctr_issue")

    if impressions > 8000 and ctr < 1:
        flags.append("intent_issue")

    return flags


# -----------------------------
# GROQ AI ANALYSIS
# -----------------------------
def groq_analysis(data):
    prompt = f"""
You are a senior SEO strategist.

Analyze this Google Search Console data:

{data}

Return:
1. Root cause
2. Exact fix (no generic advice)
3. Priority (High/Medium/Low)
4. Expected impact on traffic
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert SEO consultant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# -----------------------------
# FILE UPLOAD
# -----------------------------
file = st.file_uploader("Upload GSC CSV", type=["csv"])

if file:

    df = pd.read_csv(file)

    # LIMIT FOR SPEED (VERY IMPORTANT)
    df = df.head(25)

    st.subheader("📄 Raw Data Preview")
    st.dataframe(df, use_container_width=True)

    results = []

    # FAST LOOP
    for row in df.itertuples():

        clicks = clean_number(getattr(row, "Clicks", 0))
        impressions = clean_number(getattr(row, "Impressions", 0))
        ctr = clean_number(getattr(row, "CTR", 0))
        position = clean_number(getattr(row, "Position", 0))

        page = getattr(row, "Top_pages", None) or getattr(row, "Page", None) or "Unknown"

        # RULE FILTER FIRST
        flags = rule_engine(clicks, impressions, ctr, position)

        # AI ONLY FOR IMPORTANT ROWS
        if flags:
            ai_input = {
                "Page": page,
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Issues": flags
            }

            ai_result = groq_analysis(ai_input)
        else:
            ai_result = "No major issues detected"

        results.append({
            "Page": page,
            "Clicks": clicks,
            "Impressions": impressions,
            "CTR": ctr,
            "Position": position,
            "AI Insights": ai_result
        })

    result_df = pd.DataFrame(results)

    st.subheader("📊 AI SEO Insights")

    st.dataframe(result_df, use_container_width=True)

    st.download_button(
        "📥 Download Report",
        result_df.to_csv(index=False),
        "ai_seo_report.csv",
        mime="text/csv"
    )
