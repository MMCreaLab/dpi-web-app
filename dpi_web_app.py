#python -m streamlit run dpi_web_app.py

import streamlit as st
from PIL import Image
import io, zipfile

# ---------------- HEADER ----------------
# Load logo
logo = Image.open("RM_logo.png")

# Create two columns for layout: left for logo, right for title/description
col1, col2 = st.columns([1, 3])  # Adjust ratios for proper spacing

with col1:
    st.image(logo, width=120)  # Logo width, adjust as needed

with col2:
    st.markdown(
        """
        <div style='display:flex; flex-direction:column; justify-content:center;'>
            <h2 style='margin:0;'>Free DPI Converter 📸</h2>
            <p style='margin:0; font-size:14px; color:gray;'>
                Changes the DPI of your images (300 DPI recommended for prints).<br>
                Free tool for authors, publishers, and creators.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")  # horizontal line separator

st.write("""
Upload one or more images, choose a DPI setting, and download the converted images.  
**Tips for authors**:  
- 📚 Print books → use **300 DPI**  
- 📱 eBooks & web → use **96 DPI**
""")

# ---------------- FILE UPLOADER ----------------
uploaded_files = st.file_uploader(
    "Upload images (JPG or PNG)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

# ---------------- DPI PRESETS ----------------
st.subheader("Select Output DPI")

preset = st.radio(
    "Choose a preset:",
    ["Print (300 DPI)", "Web (96 DPI)", "Custom"],
    horizontal=True
)

if preset == "Print (300 DPI)":
    dpi = 300
elif preset == "Web (96 DPI)":
    dpi = 96
else:
    dpi = st.number_input("Enter custom DPI:", min_value=72, max_value=1200, value=300, step=1)

# ---------------- OPTIMIZATION ----------------
optimize = st.checkbox("Optimize Size/Quality (smaller file, slightly lower quality)", value=False)

# ---------------- CONVERSION ----------------
if uploaded_files:
    st.write(f"✅ {len(uploaded_files)} file(s) uploaded")

    if st.button("Convert Images"):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for uploaded_file in uploaded_files:
                img = Image.open(uploaded_file)
                output_buffer = io.BytesIO()

                # Save with DPI and optimization
                if uploaded_file.name.lower().endswith((".jpg", ".jpeg")):
                    quality = 85 if optimize else 100
                    img.save(output_buffer, format="JPEG", dpi=(dpi, dpi), quality=quality)
                else:
                    img.save(output_buffer, format="PNG", dpi=(dpi, dpi))

                zipf.writestr(uploaded_file.name, output_buffer.getvalue())

        zip_buffer.seek(0)

        st.success(f"All images converted to {dpi} DPI! 🎉")

        st.download_button(
            label="📥 Download Converted Images (ZIP)",
            data=zip_buffer,
            file_name="converted_images.zip",
            mime="application/zip"
        )

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <div style='text-align: center; font-size:13px; color: gray;'>
        <p>© Relatable Media LLC. Available for free use.</p>
        <p>If you have any comments or questions, please contact 
           <a href="mailto:info@relatable-media.com">info@relatable-media.com</a>.
        </p>
        <p><a href="https://www.relatable-media.com" target="_blank">
           Go back to www.relatable-media.com</a>
        </p>
        <br>
        <a href="https://www.buymeacoffee.com/YOUR_USERNAME" target="_blank">
            <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" 
                 alt="Buy Me A Coffee" height="40">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

