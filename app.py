from io import BytesIO
import numpy as np
import streamlit as st
import qrcode


# Main Streamlit app
def main():
    st.set_page_config(page_title="QR Code Generator", layout="wide")
    st.title("QR Codes shouldn't be hard")

    qr_name = st.text_input("Name:", "google")
    qr_data = st.text_input("Link to Encode:", "www.google.com")
    qr_size_version = st.slider("QR code size (by version)", 1, 40, 1)
    qr_error = st.selectbox(
    "Error Correction Method",
    ("ERROR_CORRECT_M", "ERROR_CORRECT_L", "ERROR_CORRECT_Q", "ERROR_CORRECT_H"))
    qr_box_size = st.number_input("Size of box", value=10, placeholder=10)
    qr_border_size = st.number_input("Size of border", value=4, placeholder=4)
    qr_fill_color = st.color_picker("Fill Color", value="#000000")
    qr_back_color = st.color_picker("Background Color", value="#FFFFFF")

    qr_fill_color_rgb = tuple(int(qr_fill_color.lstrip('#')[i:i+2], 16) for i in (0,2,4))
    qr_back_color_rgb = tuple(int(qr_back_color.lstrip('#')[i:i+2], 16) for i in (0,2,4))

    if qr_error == "ERROR_CORRECT_L":
        qr_error_formatted = qrcode.constants.ERROR_CORRECT_L
    elif qr_error == "ERROR_CORRECT_M":
        qr_error_formatted = qrcode.constants.ERROR_CORRECT_M
    elif qr_error == "ERROR_CORRECT_Q":
        qr_error_formatted = qrcode.constants.ERROR_CORRECT_Q
    elif qr_error == "ERROR_CORRECT_H":
        qr_error_formatted = qrcode.constants.ERROR_CORRECT_H


    qr = qrcode.QRCode(
    version=qr_size_version,
    error_correction=qr_error_formatted,
    box_size=qr_box_size,
    border=qr_border_size,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=qr_fill_color_rgb, back_color=qr_back_color_rgb)
    
    if st.button("Make QR Code!"):
        st.image(np.asarray(img))
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download QR Code",
            data=byte_im,
            file_name=f"qr_code_{qr_name}.png",
            mime="image/png",
            )
    
    st.text("More info about QR codes: https://www.youtube.com/watch?v=w5ebcowAJD8")
    st.text("More info about qrcode python library: https://pypi.org/project/qrcode/")

if __name__ == "__main__":
    main()
