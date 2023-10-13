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

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()


lottie_pdf_img = current_dir / "files" / "pdf_img.json"


def load_lottiefile(filepath : str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


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

