#python -m streamlit run dpi_web_app.py
import streamlit as st
from PIL import Image
import io, zipfile

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 3])

with col1:
    st.image("RM_logo.png", width=120)  # Logo (local file)

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

# ---------------- DESCRIPTION ----------------
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
        if len(uploaded_files) == 1:
            # Single file – direct download
            uploaded_file = uploaded_files[0]
            img = Image.open(uploaded_file)
            output_buffer = io.BytesIO()

            if uploaded_file.name.lower().endswith((".jpg", ".jpeg")):
                quality = 85 if optimize else 100
                img.save(output_buffer, format="JPEG", dpi=(dpi, dpi), quality=quality)
                mime = "image/jpeg"
            else:
                img.save(output_buffer, format="PNG", dpi=(dpi, dpi))
                mime = "image/png"

            output_buffer.seek(0)

            st.success(f"{uploaded_file.name} converted to {dpi} DPI! 🎉")
            st.download_button(
                label="📥 Download Converted Image",
                data=output_buffer,
                file_name=uploaded_file.name,
                mime=mime
            )

        else:
            # Multiple files – ZIP download
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for uploaded_file in uploaded_files:
                    img = Image.open(uploaded_file)
                    output_buffer = io.BytesIO()
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
    <div style='text-align: center; font-size:13px; color: gray; line-height:1.5;'>
        <p>© Relatable Media LLC. Available for free use.</p>
        <p>If you have any comments or questions, please contact 
           <a href="mailto:info@relatable-media.com">info@relatable-media.com</a>.
        </p>
        <p><a href="https://www.relatable-media.com" target="_blank">
           Go back to www.relatable-media.com</a>
        </p>
        <br>
        <a href="https://buymeacoffee.com/relatable_media" target="_blank">
            <img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" 
                 alt="Buy Me A Coffee" height="40">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

