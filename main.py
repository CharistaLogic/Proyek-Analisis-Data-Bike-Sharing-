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
    df_2012 = df[df['yr'] == 1].copy()
    
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_2012['mnth_name'] = df_2012['mnth'].map(month_map)
    
    def get_temp_category(temp_val):
        if temp_val < 0.33: return 'Cold'
        elif 0.33 <= temp_val < 0.66: return 'Moderate'
        else: return 'Hot'
    df_2012['temp_category'] = df_2012['temp'].apply(get_temp_category)
    return df_2012

df_main = load_data()

# --- SIDEBAR (FITUR INTERAKTIF UTAMA) ---
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

# Metrik Interaktif
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
        st.warning("⚠️ Pilih bulan di sidebar untuk melihat data.")

with tab2:
    st.subheader("Dampak Kecepatan Angin")
    if not filtered_df.empty:
        avg_wind = df_main['windspeed'].mean()
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(lambda x: 'Angin Tinggi' if x > avg_wind else 'Angin Rendah')
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

# --- CONCLUSION & RECOMMENDATION (INTERAKTIF) ---
st.divider()
st.subheader("Conclusion & Recommendation")

# Membuat Expander agar interaktif (bisa dibuka-tutup)
with st.expander("Klik untuk melihat Detail Kesimpulan & Rekomendasi"):
    # Menampilkan jumlah bulan yang sedang dianalisis secara dinamis
    st.write(f"### Analisis Berdasarkan {len(selected_months)} Bulan Terpilih:")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.success("**Conclusion**")
        st.write(f"""
        1. **Tren Bulanan:** Terdapat peningkatan penyewaan yang signifikan di pertengahan tahun, mencapai puncaknya di bulan September.
        2. **Kecepatan Angin:** Kondisi angin rendah terbukti menghasilkan rata-rata penyewaan sebesar **{filtered_df[filtered_df['windspeed'] < filtered_df['windspeed'].mean()]['cnt'].mean():.0f}** unit (lebih tinggi dibanding saat angin kencang).
        3. **Stabilitas Pengguna:** Pengguna *registered* memiliki pola yang jauh lebih stabil dibandingkan pengguna *casual*.
        """)

    with col_b:
        st.info("**Recommendation**")
        st.write("""
        1. **Optimalisasi Unit:** Menambah jumlah sepeda pada bulan dengan permintaan tertinggi (Mei-September).
        2. **Operasional:** Menyesuaikan operasional dan pengecekan armada berdasarkan kondisi angin harian.
        3. **Strategi Retensi:** Mengembangkan program loyalitas untuk pengguna *registered* agar stabilitas tetap terjaga.
        4. **Target Marketing:** Memberikan promo khusus untuk meningkatkan jumlah pengguna *casual* pada hari dengan cuaca cerah/suhu panas.
        """)

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
