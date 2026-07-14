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

# Fungsi untuk menampilkan logo saja (tanpa text tambahan)
def show_logo():
    # Pastikan file logo kamu bernama 'logo.png' dan sudah ada di folder yang sama dengan app.py
    if os.path.exists("logo.png"):
        st.image("logo.png", width=400)
    else:
        st.write("Logo tidak ditemukan (Upload 'logo.png' ke folder utama)")

# Database setup
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
st.subheader("Asset Management Pro")
tab1, tab2 = st.tabs(["➕ Input & Upload Asset", "🔍 Scan, Search & Print"])

# ... (Sisa kode di bawah tetap sama seperti sebelumnya) ...
# (Silakan lanjutkan dengan bagian with tab1 dan tab2 dari kode sebelumnya)