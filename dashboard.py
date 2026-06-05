import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Konfigurasi Halaman Web
st.set_page_config(page_title="Dashboard Logistik", layout="wide")
st.title("Dashboard Performa Logistik")

# 1. Buka Koneksi Database
conn = sqlite3.connect('logistics.db')

# 2. Bikin Layout Terbagi Jadi 2 Kolom (Kiri dan Kanan)
col1, col2 = st.columns(2)

# Mengisi Kolom Kiri
with col1:
    st.subheader("Proporsi Tipe Pesanan")
    query_pesanan = """
    SELECT booking_type, COUNT(load_id) as total_orderan
    FROM loads
    GROUP BY booking_type;
    """
    df_pesanan = pd.read_sql(query_pesanan, conn)
    
    # Bikin Grafik Batang bawaan Streamlit
    st.bar_chart(data=df_pesanan, x='booking_type', y='total_orderan', color="#FF4B4B")

# Mengisi Kolom Kanan
with col2:
    st.subheader("Top 5 Pelanggan Sultan")
    query_sultan = """
    SELECT 
        c.customer_name AS nama_pelanggan,
        SUM(l.revenue) AS total_kontribusi_revenue
    FROM loads l
    JOIN customers c ON l.customer_id = c.customer_id
    GROUP BY c.customer_name
    ORDER BY total_kontribusi_revenue DESC
    LIMIT 5;
    """
    df_sultan = pd.read_sql(query_sultan, conn)
    
    # Bikin Grafik Batang bawaan Streamlit
    st.bar_chart(data=df_sultan, x='nama_pelanggan', y='total_kontribusi_revenue', color="#0068C9")

# Mengisi Komposisi Merk Truk di Bawah
st.write("---") #garis batas
st.subheader("Komposisi Merk Truk")
query_truk = """
SELECT make AS merk, COUNT(truck_id) as jumlah_truk
FROM trucks
GROUP BY make
ORDER BY jumlah_truk DESC;
"""
df_truk = pd.read_sql(query_truk, conn)

# Bikin Grafik Batang bawaan Streamlit
#st.bar_chart(data=df_truk, x='merk', y='jumlah_truk', color="#FFD700")
#st.bar_chart(df_truk.set_index('merk'))

# Bikin grafik rapih urut berdasarkan jumlah truk dengan warna yang lebih menarik menggunakan Plotly
fig = px.bar(df_truk, x='merk', y='jumlah_truk', color='merk', text_auto=True)

st.plotly_chart(fig, use_container_width=True)

#
st.write("---") #garis batas
st.subheader("Top Pelanggan per Tipe Pesanan")

# membuat dropdown untuk memilih tipe pesanan
pilihan_tipe = st.selectbox("Pilih Tipe Pesanan", df_pesanan['booking_type'].unique())

# query untuk mendapatkan top pelanggan berdasarkan tipe pesanan yang dipilih
query_top_pelanggan = f"""
SELECT
    c.customer_name AS nama_pelanggan,
    SUM(l.revenue) AS total_kontribusi_revenue
FROM loads l
JOIN customers c ON l.customer_id = c.customer_id
WHERE l.booking_type = '{pilihan_tipe}'
GROUP BY c.customer_name
ORDER BY total_kontribusi_revenue DESC
LIMIT 5;
"""
# menerjemahkan query ke dalam DataFrame
df_top_pelanggan = pd.read_sql(query_top_pelanggan, conn)

# menampilkan grafik batang untuk top pelanggan berdasarkan tipe pesanan yang dipilih
fig_top_pelanggan = px.bar(
    df_top_pelanggan, 
    x='nama_pelanggan', 
    y='total_kontribusi_revenue', 
    color='nama_pelanggan', 
    text_auto=True
)

st.plotly_chart(fig_top_pelanggan, use_container_width=True)

# Tutup koneksi database agar memori tetap hemat
conn.close()