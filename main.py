import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 2. Fungsi Memuat Data
@st.cache_data
def load_data():
    # Pastikan file day.csv ada di folder yang sama
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Filter Tahun 2012
    df_2012 = df[df['yr'] == 1].copy()
    
    # Mapping Nama Bulan
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_2012['mnth_name'] = df_2012['mnth'].map(month_map)
    
    # Kategori Suhu
    def get_temp_category(temp_val):
        if temp_val < 0.33: return 'Cold'
        elif 0.33 <= temp_val < 0.66: return 'Moderate'
        else: return 'Hot'
    df_2012['temp_category'] = df_2012['temp'].apply(get_temp_category)
    
    return df_2012

df_main = load_data()

# --- SIDEBAR (FITUR INTERAKTIF) ---
st.sidebar.title("🚲 Opsi Filter")
month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_months = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=month_options,
    default=month_options
)

# Filter Data
filtered_df = df_main[df_main['mnth_name'].isin(selected_months)]

# --- HALAMAN UTAMA ---
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# Metrik
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Suhu", f"{filtered_df['temp'].mean():.2f}")
with col3:
    st.metric("Rata-rata Kecepatan Angin", f"{filtered_df['windspeed'].mean():.2f}")

st.divider()

# --- VISUALISASI ---
tab1, tab2, tab3 = st.tabs(["Tren & Tipe User", "Dampak Angin", "Kategori Suhu"])

with tab1:
    st.subheader("Tren Bulanan & Perbandingan Pengguna")
    if not filtered_df.empty:
        actual_order = [m for m in month_options if m in selected_months]
        trend_data = filtered_df.groupby('mnth_name')[['casual', 'registered', 'cnt']].mean().reindex(actual_order)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(trend_data.index, trend_data['cnt'], marker='o', label='Total', color='green')
        ax.bar(trend_data.index, trend_data['registered'], alpha=0.3, label='Registered', color='blue')
        ax.bar(trend_data.index, trend_data['casual'], alpha=0.3, label='Casual', color='orange')
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Silakan pilih bulan di sidebar.")

with tab2:
    st.subheader("Penyewaan Berdasarkan Kecepatan Angin")
    if not filtered_df.empty:
        avg_wind = df_main['windspeed'].mean()
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(lambda x: 'Tinggi' if x > avg_wind else 'Rendah')
        wind_impact = filtered_df.groupby('wind_status')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_impact.index, y=wind_impact.values, palette='viridis', ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)

with tab3:
    st.subheader("Analisis Berdasarkan Kategori Suhu")
    if not filtered_df.empty:
        actual_order = [m for m in month_options if m in selected_months]
        temp_analysis = filtered_df.groupby(['mnth_name', 'temp_category'])['cnt'].mean().unstack().reindex(actual_order)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        temp_analysis.plot(kind='bar', ax=ax)
        ax.set_ylabel("Jumlah Penyewaan")
        st.pyplot(fig)

# --- CONCLUSION & RECOMMENDATION ---
st.divider()
st.subheader("Conclusion & Recommendation")

st.markdown("""
- **Kesimpulan 1:** Tren peningkatan penyewaan terjadi di pertengahan tahun (puncaknya September).
- **Kesimpulan 2:** Angin rendah menghasilkan penyewaan lebih tinggi karena faktor kenyamanan.
- **Kesimpulan 3:** Pengguna *registered* jauh lebih stabil dibanding *casual*.

**Rekomendasi:**
1. Tambah stok sepeda di bulan Mei-September.
2. Berikan promo untuk menarik pengguna *casual* saat cuaca hangat.
3. Kembangkan program retensi bagi pengguna *registered*.
""")

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
