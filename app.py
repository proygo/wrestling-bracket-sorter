import streamlit as st
from parser import extract_wrestlers_from_html

st.title("TrackWrestling Bracket Parser")

uploaded_file = st.file_uploader("Upload a TrackWrestling bracket HTML file")

if uploaded_file:
    # Save to temporary file
    with open("temp.html", "wb") as f:
        f.write(uploaded_file.read())
    
    wrestlers = extract_wrestlers_from_html("temp.html")
    st.write("### Wrestlers Found:")
    st.write(wrestlers)

    # Optionally allow download
    st.download_button("Download Wrestlers List", "\n".join(wrestlers), file_name="wrestlers.txt")
