import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman & Judul
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 2. Fungsi Memuat Data (Sesuai dengan alur analisis Anda)
@st.cache_data
def load_data():
    # Pastikan file day.csv ada di folder yang sama dengan script ini
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Filter Tahun 2012 (yr=1) sesuai ruang lingkup analisis Anda
    df_2012 = df[df['yr'] == 1].copy()
    
    # Mapping Nama Bulan agar Interaktif & User-Friendly
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_2012['mnth_name'] = df_2012['mnth'].map(month_map)
    
    # Kategori Suhu (Sesuai fungsi get_temp_category di notebook Anda)
    def get_temp_category(temp_val):
        if temp_val < 0.33: return 'Cold'
        elif 0.33 <= temp_val < 0.66: return 'Moderate'
        else: return 'Hot'
    df_2012['temp_category'] = df_2012['temp'].apply(get_temp_category)
    
    return df_2012

# Memasukkan data ke aplikasi
df_main = load_data()

# --- SIDEBAR (FITUR INTERAKTIF: FILTERING BULAN) ---
st.sidebar.title("🚲 Opsi Filter")
st.sidebar.markdown("Gunakan filter di bawah ini untuk memanipulasi data pada dashboard secara real-time.")

month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_months = st.sidebar.multiselect(
    "Pilih Bulan untuk Dianalisis:",
    options=month_options,
    default=month_options
)

# Terapkan Filter Berdasarkan Pilihan User
filtered_df = df_main[df_main['mnth_name'].isin(selected_months)]

# --- HALAMAN UTAMA ---
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# Metrik Utama sebagai Ringkasan Cepat
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Suhu (Norm)", f"{filtered_df['temp'].mean():.2f}")
with col3:
    st.metric("Rata-rata Kecepatan Angin", f"{filtered_df['windspeed'].mean():.2f}")

st.divider()

# --- VISUALISASI DATA (Menjawab Pertanyaan Bisnis) ---
st.subheader("Hasil Eksplorasi Data")

tab1, tab2, tab3 = st.tabs(["Tren & Tipe Pengguna", "Kondisi Angin", "Kategori Suhu"])

with tab1:
    st.write("### Tren Rata-rata Penyewaan per Bulan (2012)")
    if not filtered_df.empty:
        # Urutan bulan kronologis sesuai pilihan user
        actual_order = [m for m in month_options if m in selected_months]
        trend_data = filtered_df.groupby('mnth_name')[['casual', 'registered', 'cnt']].mean().reindex(actual_order)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(trend_data.index, trend_data['cnt'], marker='o', linewidth=2, label='Total', color='#2E7D32')
        ax.bar(trend_data.index, trend_data['registered'], alpha=0.3, label='Registered', color='#1976D2')
        ax.bar(trend_data.index, trend_data['casual'], alpha=0.3, label='Casual', color='#F57C00')
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("⚠️ Harap pilih minimal satu bulan di sidebar.")

with tab2:
    st.write("### Perbandingan Penyewaan Berdasarkan Kecepatan Angin")
    if not filtered_df.empty:
        avg_wind_ref = df_main['windspeed'].mean()
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(lambda x: 'Angin Tinggi' if x > avg_wind_ref else 'Angin Rendah')
        wind_impact = filtered_df.groupby('wind_status')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_impact.index, y=wind_impact.values, palette='viridis', ax=ax)
        st.pyplot(fig)

with tab3:
    st.write("### Rata-rata Penyewaan per Kategori Suhu")
    if not filtered_df.empty:
        actual_order = [m for m in month_options if m in selected_months]
        temp_analysis = filtered_df.groupby(['mnth_name', 'temp_category'])['cnt'].mean().unstack().reindex(actual_order)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        temp_analysis.plot(kind='bar', ax=ax, color=['#81C784', '#4CAF50', '#1B5E20'])
        ax.set_ylabel("R
