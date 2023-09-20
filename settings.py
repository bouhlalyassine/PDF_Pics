import json
from pathlib import Path
from PIL import Image
import requests
import io
from pikepdf import Pdf, PdfImage
import plotly.express as px
import zipfile
import numpy as np
import plotly.express as px
import streamlit as st
import os
import base64


TITLE = "PDF Pics"
PAGE_ICON ="ico_potfolio.ico"

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

css_file = current_dir / "main.css"

# My Tuto :
space = 15
tuto_space = 70

tuto_extr_img_p = current_dir / "files" / "tuto_ext_img_pdf.mp4"
tuto_extr_img = str(tuto_extr_img_p)

pp_logo_portfolio = current_dir / "files" /  "logo_portfolio.png"
linkpic_code = current_dir / "files" /  "code.png"

lottie_pdf_img = current_dir / "files" / "pdf_img.json"


def load_lottiefile(filepath : str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Clickable img
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data
def get_img_with_href(local_img_path, target_url, width, loc):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_{loc}" style="display: flex; justify-content: center; align-items: center;">
            <img src="data:image/{img_format};base64,{bin_str}" width="{width}" class="img-hover-effect">
        </a>'''
    return html_code


def extract_img(pdf):
    images = []
    doc_pdf = Pdf.open(pdf)
    for i, page in enumerate(doc_pdf.pages):
        for j, (name, raw_image) in enumerate(page.images.items()):
            image = PdfImage(raw_image)
            images.append(image.as_pil_image())
    return images

def resize_image(img):
    w = int(img.size[0])
    if w > 500 :
        width = 500
    else :
        width= w
    return width

def disp_chart_img(img_displ):
    img_displ = np.array(img_displ)
    img_displ = np.array(Image.fromarray(img_displ).convert('RGB'))

    img = px.imshow(img_displ)
    img.update_layout(
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    xaxis_visible=False,
    yaxis_visible=False)

    return img

def generate_zip_file(imgz):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for i, img in enumerate(imgz):
            img_buffer = io.BytesIO()
            try :
                img.save(img_buffer, format="JPEG")
            except :
                img.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            zip_file.writestr(f"img_{i+1}.png", img_buffer.read())
    buffer.seek(0)
    return buffer.read()

