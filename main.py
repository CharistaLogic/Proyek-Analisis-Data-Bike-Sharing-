import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 2. Fungsi Memuat Data
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Filter Tahun 2012 sesuai analisis notebook
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

# Filter Data Berdasarkan Sidebar
filtered_df = df_main[df_main['mnth_name'].isin(selected_months)]

# --- HALAMAN UTAMA ---
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# Metrik Dinamis
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Kelembapan", f"{filtered_df['hum'].mean():.2f}")
with col3:
    st.metric("Rata-rata Kecepatan Angin", f"{filtered_df['windspeed'].mean():.2f}")

st.divider()

# --- VISUALISASI DATA ---
tab1, tab2, tab3 = st.tabs(["Tren & User", "Dampak Angin", "Kategori Suhu"])

with tab1:
    st.subheader("Tren Bulanan & Perbandingan Pengguna")
    if not filtered_df.empty:
        actual_order = [m for m in month_options if m in selected_months]
        trend_data = filtered_df.groupby('mnth_name')[['casual', 'registered', 'cnt']].mean().reindex(actual_order)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(trend_data.index, trend_data['cnt'], marker='o', label='Total', color='#2E7D32')
        ax.bar(trend_data.index, trend_data['registered'], alpha=0.3, label='Registered', color='#1976D2')
        ax.bar(trend_data.index, trend_data['casual'], alpha=0.3, label='Casual', color='#F57C00')
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Silakan pilih bulan di sidebar.")

with tab2:
    st.subheader("Dampak Kecepatan Angin")
    if not filtered_df.empty:
        avg_wind_ref = df_main['windspeed'].mean()
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(lambda x: 'Angin Tinggi' if x > avg_wind_ref else 'Angin Rendah')
        wind_impact = filtered_df.groupby('wind_status')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_impact.index, y=wind_impact.values, palette='viridis', ax=ax)
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

# --- BAGIAN INTERAKTIF: CONCLUSION & RECOMMENDATION ---
st.divider()
st.subheader("Conclusion & Recommendation")

# Menggunakan expander agar user bisa melakukan aksi klik (interaktif)
with st.expander("Klik untuk melihat Detail Analisis & Rekomendasi"):
    # Menampilkan informasi dinamis sesuai jumlah bulan yang dipilih
    st.write(f"### Analisis Berdasarkan {len(selected_months)} Bulan Terpilih")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.success("**Conclusion**")
        st.write(f"""
        1. **Tren Bulanan:** Terdapat tren peningkatan penyewaan yang signifikan terutama di pertengahan tahun (puncaknya pada bulan September).
        2. **Kecepatan Angin:** Kondisi angin rendah menghasilkan rata-rata penyewaan sebesar **{filtered_df[filtered_df['windspeed'] < df_main['windspeed'].mean()]['cnt'].mean():.0f}** unit (lebih tinggi dibanding saat angin kencang).
        3. **Pola Pengguna:** Pengguna *registered* memiliki pola penggunaan yang stabil dengan rata-rata harian **{filtered_df['registered'].mean():.0f}** penyewaan.
        """)

    with col_right:
        st.info("**Recommendation**")
        st.write("""
        - **Optimalisasi Stok:** Menambah jumlah unit sepeda pada bulan dengan permintaan tertinggi (Mei-September).
        - **Operasional Cuaca:** Menyesuaikan jadwal pengecekan sepeda pada hari dengan prediksi angin rendah untuk mengantisipasi lonjakan.
        - **Strategi Loyalitas:** Mengembangkan program retensi khusus untuk pengguna *registered* agar stabilitas penyewaan terjaga.
        - **Promo Casual:** Memberikan diskon khusus untuk pengguna *casual* pada kategori suhu *Moderate* hingga *Hot*.
        """)

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
