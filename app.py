import streamlit as st
import pytesseract
from PIL import Image
import re
from collections import defaultdict

st.title("🏆 Wrestling Bracket Grade Sorter")
st.write("Upload a bracket image (JPG/PNG) with grade info like `SMNW, 11` and wrestler names.")

# Upload image
uploaded_file = st.file_uploader("Choose a bracket image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Bracket", use_column_width=True)

    # Extract text with OCR
    with st.spinner("🔍 Extracting text..."):
        text = pytesseract.image_to_string(image)

    # Parse names and grades
    grade_groups = defaultdict(list)
    matches = re.findall(r"([A-Z][a-zA-Z.'\-]+(?:\s+[A-Z][a-zA-Z.'\-]+)+),\s+[A-Z]+,\s*(9|10|11|12)", text)

    for name, grade in matches:
        grade_groups[int(grade)].append(name.strip())

    # Display results
    if grade_groups:
        st.success("✅ Wrestlers sorted by grade:")
        for grade in sorted(grade_groups):
            st.subheader(f"Grade {grade}")
            for name in sorted(set(grade_groups[grade])):
                st.write(f"- {name}")
    else:
        st.warning("⚠️ No valid wrestler entries detected. Try a clearer image or PDF.")



