import streamlit as st
from settings import *
from streamlit_lottie import st_lottie
import streamlit as st
from io import BytesIO


# streamlit run Extract_PDF_Images.py

st.set_page_config(page_title=TITLE,
    layout="wide")


st.markdown("<h2 style=\
        'text-align : center';\
        font-weight : bold ;\
        font-family : Arial;>\
        Extract Images from PDF</h2>", unsafe_allow_html=True)
st.markdown("---")

with st.sidebar :
    uploaded_file = st.file_uploader("📌 Upload PDF", type=["pdf"], key="fup1", label_visibility="visible")


if uploaded_file :
    images = extract_img(uploaded_file)
    namefile = uploaded_file.name
    img_idx = 0
    all_images = []
    
    with st.spinner("Extraction in progress, please wait..."):
        for image in images:
            all_images.append(image)

    if len(images)==0:
        st.error("No image detected")

    else :
        colpi1, colpi2, colpi3 = st.columns([41, 18, 41], gap="small")

        with colpi2:
            st.markdown(f"<h5 style=\
            'text-align : left';\
            font-weight : bold ;\
            font-family : Arial;>\
            <b>{len(all_images)} Images detected</h5></b>", unsafe_allow_html=True)

            img_idx = st.number_input(label="Label", value=1, min_value=1, max_value=len(all_images),
                step=1, label_visibility="collapsed")

        with colpi3:
            zip_file_name = f"Images_{uploaded_file.name[:-4]}.zip" 
            zip_file = generate_zip_file(all_images)

            st.download_button(
                label = "Download All images",
                data = zip_file,
                file_name = zip_file_name,
                mime = "application/zip")

        img_displ = all_images[img_idx - 1]
        
        with colpi1:
            try :
                buf = BytesIO()
                img_displ.save(buf, format="JPEG")
                byte_im = buf.getvalue()
            except:
                buf = BytesIO()
                img_displ.save(buf, format="PNG")
                byte_im = buf.getvalue()

            st.download_button(
                label="Download this image",
                data=byte_im,
                file_name=f"image_{img_idx}.png",
                mime="image")
        
        img_width = resize_image(img_displ)
        img_chart = st.image(image = img_displ, width = img_width)

else:
    st.markdown("<br>", unsafe_allow_html=True)
    colpi_1, colpi_2 = st.columns([85, 15], gap="small")
    with colpi_1 :
        st.info("This tool allows you to extract images from a PDF : \
            \n ● View them individually\
            \n ● Download them, while keeping their original quality\
            \n\n You can upload the PDF to be processed on the left menu")

    with colpi_2:
        lottie_pdfimg = load_lottiefile(lottie_pdf_img)
        st_lottie(
        lottie_pdfimg,
        speed=1,
        reverse=False,
        loop=True,
        quality="high",
        height=150)