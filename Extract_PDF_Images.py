import streamlit as st
from settings import *
from streamlit_lottie import st_lottie
import streamlit as st
from io import BytesIO


# streamlit run Extract_PDF_Images.py

st.set_page_config(page_title=TITLE,
    page_icon=PAGE_ICON,
    layout="wide")

# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f: # Load the CSS file
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)


st.markdown("<h2 style=\
        'text-align : center';\
        font-weight : bold ;\
        font-family : Arial;>\
        Extract Images from PDF</h2>", unsafe_allow_html=True)
st.markdown("---")

with st.sidebar :
    clickable_img_logo = get_img_with_href(pp_logo_portfolio, 'https://ybouhlal.streamlit.app/', 70, "blank")
    st.markdown(clickable_img_logo, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    clickable_img = get_img_with_href(linkpic_code, 'https://github.com/bouhlalyassine/PDF_Pics',
        170, "blank")
    st.markdown(clickable_img, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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
        
        # img = disp_chart_img(img_displ)
        # img_chart= st.plotly_chart(img, use_container_width=True)
        img_width = resize_image(img_displ)
        img_chart = st.image(image = img_displ, width = img_width) # use_column_width=True

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
        quality="high", # medium ; high ; low
        height=150)

    esp_1, col_vid_tuto, esp_2 = st.columns([space, tuto_space, space], gap="small")
    with col_vid_tuto :
        with open(tuto_extr_img, "rb") as tuto_file:
            tuto_extr_img_byte = tuto_file.read()
        st.video(tuto_extr_img_byte)