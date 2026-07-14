import streamlit as st
import sqlite3
import pandas as pd
import qrcode
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
import os

# --- CONFIG ---
st.set_page_config(page_title="Waskita Asset Management", layout="wide")
os.makedirs("images", exist_ok=True)

# Fungsi untuk menampilkan logo agar rapi
def show_logo():
    if os.path.exists("logo.png"):
        st.image("logo.png", width=300)
    else:
        st.title("🏗️ PT. Waskita Niagaprima")

# Database setup (tetap sama)
def init_db():
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
                    asset_id TEXT PRIMARY KEY, asset_name TEXT, brand TEXT, model_type TEXT, 
                    serial_number TEXT, category TEXT, sub_category TEXT, item_type TEXT, 
                    qty INTEGER, uom TEXT, condition TEXT, current_status TEXT, 
                    current_project TEXT, current_pic TEXT, no_transmittal TEXT, 
                    current_area TEXT, current_location TEXT, storage_type TEXT, 
                    cabinet_rack TEXT, shelf TEXT, bin TEXT, purchase_date TEXT, 
                    supplier TEXT, po_number TEXT, purchase_price REAL, remark TEXT, image_filename TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- LOGIN ---
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if not st.session_state["logged_in"]:
    show_logo()
    st.subheader("Login Asset Management")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "wnp123":
            st.session_state["logged_in"] = True
            st.rerun()
        else: st.error("Username atau Password salah!")
    st.stop()

# --- MAIN APP ---
show_logo()
st.subheader("Asset Management Pro - PT. Waskita Niagaprima")
tab1, tab2 = st.tabs(["➕ Input & Upload Asset", "🔍 Scan, Search & Print"])

with tab1:
    with st.form("input_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            aid = st.text_input("Asset ID")
            name = st.text_input("Asset Name")
            brand = st.text_input("Brand")
            model = st.text_input("Model/Type")
            serial = st.text_input("Serial Number")
            cat = st.text_input("Category")
        with c2:
            subcat = st.text_input("Sub Category")
            itemtype = st.text_input("Item Type")
            qty = st.number_input("Qty", value=1)
            uom = st.text_input("UOM")
            cond = st.text_input("Condition")
            status = st.text_input("Current Status")
        with c3:
            proj = st.text_input("Current Project")
            pic = st.text_input("Current PIC")
            trans = st.text_input("No. Transmittal")
            area = st.text_input("Current Area")
            loc = st.text_input("Current Location")
            stype = st.text_input("Storage Type")
        
        c4, c5, c6 = st.columns(3)
        with c4:
            rack = st.text_input("Cabinet/Rack")
            shelf = st.text_input("Shelf")
            bin = st.text_input("Bin")
        with c5:
            pdate = st.text_input("Purchase Date")
            supp = st.text_input("Supplier")
            po = st.text_input("PO Number")
        with c6:
            price = st.number_input("Purchase Price", value=0.0)
            rem = st.text_area("Remark")
            uploaded_file = st.file_uploader("Upload Foto Barang", type=["jpg", "png", "jpeg"])
            
        if st.form_submit_button("Simpan Data"):
            filename = None
            if uploaded_file:
                filename = f"img_{aid}.png"
                Image.open(uploaded_file).save(os.path.join("images", filename))
            
            conn = sqlite3.connect('assets.db')
            try:
                conn.execute("INSERT INTO assets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                             (aid, name, brand, model, serial, cat, subcat, itemtype, qty, uom, cond, status, proj, pic, trans, area, loc, stype, rack, shelf, bin, pdate, supp, po, price, rem, filename))
                conn.commit()
                st.success(f"Data {aid} berhasil disimpan!")
            except Exception as e: st.error(f"Error: {e}")
            conn.close()

with tab2:
    img = st.camera_input("Scan QR Code")
    found_id = ""
    if img:
        bytes_data = img.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        found_id = cv2.QRCodeDetector().detectAndDecode(cv2_img)[0]
        if found_id: st.success(f"Ditemukan: {found_id}")
    
    search_q = st.text_input("Cari:", value=found_id)
    if search_q:
        conn = sqlite3.connect('assets.db')
        df = pd.read_sql(f"SELECT * FROM assets WHERE asset_id LIKE '%{search_q}%' OR asset_name LIKE '%{search_q}%'", conn)
        conn.close()
        if not df.empty:
            for _, row in df.iterrows():
                with st.expander(f"📦 {row['asset_id']} - {row['asset_name']}"):
                    st.write(row.to_dict())
                    qr = qrcode.make(row['asset_id'])
                    buf = BytesIO()
                    qr.save(buf, format="PNG")
                    st.image(buf, width=100)
                    st.download_button(f"Download QR", buf.getvalue(), f"{row['asset_id']}_QR.png")
        else: st.warning("Data tidak ditemukan.")