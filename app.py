import streamlit as st
import pandas as pd
from retriever import search
from utils import extract_text_from_url, refine_query_with_gemini

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")
st.title("SHL Assessment Recommendation Engine")

input_mode = st.radio("Choose Input Type:", ["Text Query", "JD URL"])

if input_mode == "Text Query":
    user_input = st.text_area("Enter Job Description or Query", height=200)
else:
    user_input = st.text_input("Paste Job Description URL")

if st.button("🔍 Recommend Assessments") and user_input:
    with st.spinner("Processing..."):

        if input_mode == "JD URL":
            jd_text = extract_text_from_url(user_input)
            query = refine_query_with_gemini(jd_text)
            st.markdown(f"**🔎 Refined Query:** `{query}`")
        else:
            query = refine_query_with_gemini(user_input)
            st.markdown(f"**🔎 Refined Query:** `{query}`")

        results = search(query)

    if results:
        st.success(f"Top {len(results)} recommendations:")
        table_data = []
        for r in results:
            table_data.append({
                "Assessment Title": r["title"],
                "Duration (min)": r["assessment_length_minutes"],
                "Test Types": ", ".join(r["test_type"]),
                "Remote Testing": r["remote_testing"],
                "Adaptive": r["adaptive"],
                "More Info": r["url"]
            })

        df = pd.DataFrame(table_data)

        st.markdown("### 🧾 Recommended Assessments (with clickable URLs)")
        def make_clickable(link):
            return f'<a href="{link}" target="_blank">{link}</a>'

        df["More Info"] = df["More Info"].apply(make_clickable)

        html_table = df.to_html(escape=False, index=False)
        st.markdown(html_table, unsafe_allow_html=True)

    else:
        st.warning("No relevant assessments found.")
