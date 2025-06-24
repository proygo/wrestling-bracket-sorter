# app.py
import streamlit as st
import pandas as pd
from scraper import scrape_wrestlers

st.set_page_config(layout="wide")
st.title("Trackwrestling Bracket Scraper")

st.markdown("""
Paste the **Trackwrestling bracket viewer URL** below (e.g. Kansas 6A state brackets)  
and click **Scrape Wrestlers**.  
The app will scrape all weight classes and show wrestler info.
""")

tournament_url = st.text_input("Tournament Bracket URL", 
    value="https://www.trackwrestling.com/predefinedtournaments/MainFrame.jsp?newSession=false&TIM=1750793545778&pageName=%2Fpredefinedtournaments%2FBracketViewer.jsp&twSessionId=gpewflalse")

if st.button("Scrape Wrestlers"):
    if not tournament_url:
        st.error("Please enter a valid Trackwrestling bracket URL.")
    else:
        with st.spinner("Scraping brackets... This can take up to 30 seconds"):
            try:
                df = scrape_wrestlers(tournament_url)
                if df.empty:
                    st.warning("No wrestlers found. Check the URL or try again later.")
                else:
                    st.success(f"Found {len(df)} wrestlers!")
                    st.dataframe(df)

                    grade_filter = st.multiselect("Filter by Grade", options=sorted(df["Grade"].unique()))
                    weight_filter = st.multiselect("Filter by Weight Class", options=sorted(df["Weight Class"].unique()))

                    filtered_df = df[
                        (df["Grade"].isin(grade_filter) if grade_filter else True) &
                        (df["Weight Class"].isin(weight_filter) if weight_filter else True)
                    ]

                    st.write("### Filtered Wrestlers")
                    st.dataframe(filtered_df)

                    csv = filtered_df.to_csv(index=False)
                    st.download_button("Download CSV", csv, file_name="wrestlers.csv")
            except Exception as e:
                st.error(f"Error during scraping: {e}")
