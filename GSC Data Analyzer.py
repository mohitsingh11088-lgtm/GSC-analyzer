import streamlit as st
import pandas as pd
from openai import OpenAI

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI SEO Intelligence", layout="wide")

st.title("🚀 AI SEO Content Intelligence (Groq Powered)")
st.caption("Hybrid SEO Engine: Rules + AI Insights")

# -----------------------------
# GROQ API KEY (PUT HERE)
# -----------------------------
GROQ_API_KEY = "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"

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

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
# BASIC RULE ENGINE (FILTER)
# -----------------------------
def rule_engine(clicks, impressions, ctr, position):

    flags = []

    if position > 15:
        flags.append("ranking_issue")

    if position <= 10 and ctr < 2:
        flags.append("ctr_issue")

    if impressions > 10000 and ctr < 1:
        flags.append("intent_issue")

    return flags


# -----------------------------
# GROQ AI ANALYSIS
# -----------------------------
def groq_analysis(data):

    prompt = f"""
You are a senior SEO strategist.

Analyze this Google Search Console row:

{data}

Return:
1. Root cause
2. Exact fix (no generic advice)
3. Priority (High/Medium/Low)
4. Expected impact
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

    st.subheader("📄 Raw Data")
    st.dataframe(df, use_container_width=True)

    results = []

    for _, row in df.iterrows():

        clicks = clean_number(row.get("Clicks", 0))
        impressions = clean_number(row.get("Impressions", 0))
        ctr = clean_number(row.get("CTR", 0))
        position = clean_number(row.get("Position", 0))

        page = row.get("Top pages") or row.get("Page") or "Unknown"

        # -----------------------------
        # STEP 1: RULE FILTER
        # -----------------------------
        flags = rule_engine(clicks, impressions, ctr, position)

        # Only send important rows to AI
        if flags:

            ai_input = {
                "Page": page,
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Detected Issues": flags
            }

            # -----------------------------
            # STEP 2: GROQ AI ANALYSIS
            # -----------------------------
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

    # Download
    st.download_button(
        "📥 Download Report",
        result_df.to_csv(index=False),
        "ai_seo_report.csv",
        mime="text/csv"
    )
