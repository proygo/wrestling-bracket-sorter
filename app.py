import streamlit as st
from scraper import scrape_wrestlers

st.set_page_config(layout="wide")
st.title("Kansas 6A State Wrestling Bracket Viewer")

if st.button("Scrape Wrestlers"):
    with st.spinner("Scraping brackets from Trackwrestling..."):
        df = scrape_wrestlers()
        st.success("Done!")
        st.dataframe(df)

        grade_filter = st.multiselect("Filter by Grade", options=sorted(df["Grade"].unique()))
        weight_filter = st.multiselect("Filter by Weight Class", options=sorted(df["Weight Class"].unique()))

        filtered_df = df[
            (df["Grade"].isin(grade_filter) if grade_filter else True) &
            (df["Weight Class"].isin(weight_filter) if weight_filter else True)
        ]

        st.write("### Filtered Wrestlers")
        st.dataframe(filtered_df)

        st.download_button("Download CSV", filtered_df.to_csv(index=False), file_name="wrestlers_filtered.csv")
