#python -m streamlit run dpi_web_app.py

import streamlit as st
from PIL import Image
import io, zipfile

from PIL import Image

# --- HEADER SECTION ---
# Load logo
logo = Image.open("RM_logo.png")

# Create two columns for layout
col1, col2 = st.columns([1, 3])  # left (logo), right (title)

with col1:
    st.image(logo, width=120)  # adjust width as needed

with col2:
    st.title("Relatable Media – Free DPI Converter")
    st.markdown(
        """
        Convert your images to **300 DPI** for print.  
        Free tool for authors, publishers, and creators.
        """
    )

st.markdown("---")  # horizontal line separator
st.set_page_config(page_title="Free Image DPI Converter for Authors", page_icon="📸")

st.title("📸 Free Image DPI Converter for Authors")
st.write(
    """
Upload one or more images, choose a DPI setting, and download the converted images.  
**Tips for authors**:  
- 📚 Print books → use **300 DPI**  
- 📱 eBooks & web → use **96 DPI**
"""
)

# --- File uploader (multiple files allowed) ---
uploaded_files = st.file_uploader(
    "Upload images (JPG or PNG)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

# --- DPI Presets ---
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

# --- Optimization option ---
optimize = st.checkbox("Optimize Size/Quality (smaller file, slightly lower quality)", value=False)

# --- Conversion ---
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

# --- Footer ---
st.markdown("---")
st.caption("Made with ❤️ to help indie authors prepare images for print and eBooks. Powered by Streamlit + Pillow.")
