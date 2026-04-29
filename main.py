import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 2. Fungsi Memuat Data (Sesuai dengan analisis di Notebook Anda)
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Filter Tahun 2012 (yr=1) sesuai ruang lingkup proyek Anda
    df_2012 = df[df['yr'] == 1].copy()
    
    # Mapping Nama Bulan agar Filter Sidebar lebih mudah dipahami
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_2012['mnth_name'] = df_2012['mnth'].map(month_map)
    
    return df_2012

df_main = load_data()

# --- SIDEBAR (FITUR INTERAKTIF: FILTERING) ---
st.sidebar.title("🚲 Opsi Filter")
st.sidebar.markdown("Manipulasi data dashboard dengan memilih bulan di bawah ini:")

month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_months = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=month_options,
    default=month_options
)

# Filter Data Berdasarkan Sidebar (Real-time Manipulation)
filtered_df = df_main[df_main['mnth_name'].isin(selected_months)]

# --- HALAMAN UTAMA ---
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# Metrik Utama (Dinamis mengikuti Filter)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata User Registered", f"{filtered_df['registered'].mean():.0f}")
with col3:
    st.metric("Rata-rata User Casual", f"{filtered_df['casual'].mean():.0f}")

st.divider()

# --- VISUALISASI DATA (2 Pertanyaan Bisnis Utama) ---
tab1, tab2 = st.tabs(["Tren Bulanan & Tipe User", "Dampak Kecepatan Angin"])

with tab1:
    st.subheader("Tren Rata-rata Penyewaan per Bulan (2012)")
    if not filtered_df.empty:
        # Menampilkan perbandingan Registered vs Casual sesuai analisis notebook
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
        st.warning("⚠️ Silakan pilih minimal satu bulan di sidebar.")

with tab2:
    st.subheader("Penyewaan Berdasarkan Kecepatan Angin")
    if not filtered_df.empty:
        # Logika: Membandingkan angin di atas vs di bawah rata-rata (Sesuai Pertanyaan Bisnis 3 di Notebook)
        avg_wind_ref = df_main['windspeed'].mean()
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(lambda x: 'Angin Tinggi' if x > avg_wind_ref else 'Angin Rendah')
        wind_impact = filtered_df.groupby('wind_status')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_impact.index, y=wind_impact.values, palette='viridis', ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)

# --- CONCLUSION & RECOMMENDATION (INTERAKTIF) ---
st.divider()
st.subheader("Conclusion & Recommendation")

# Fitur Interaktif: Expander untuk eksplorasi detail
with st.expander("Lihat Detail Analisis Berdasarkan Pilihan Anda"):
    st.write(f"Berikut adalah ringkasan untuk **{len(selected_months)} bulan** yang Anda pilih:")
    
    col_c, col_r = st.columns(2)
    with col_c:
        st.success("**Conclusion**")
        # Nilai rata-rata dinamis sesuai filter yang dipilih user
        avg_rent = filtered_df['cnt'].mean()
        st.write(f"""
        1. Tren mencapai puncak pada bulan September. Rata-rata penyewaan pada periode terpilih adalah **{avg_rent:.0f}** unit.
        2. Kondisi angin rendah terbukti memberikan kontribusi penyewaan yang lebih tinggi secara konsisten.
        3. Pengguna Registered mendominasi penggunaan dengan pola yang lebih stabil dibandingkan Casual.
        """)
    
    with col_r:
        st.info("**Recommendation**")
        st.write("""
        - Menambah ketersediaan armada pada bulan Mei-September (permintaan puncak).
        - Fokus strategi retensi pada pengguna Registered agar tetap loyal.
        - Memberikan promo "Cuaca Cerah" untuk menarik pengguna Casual saat angin rendah.
        """)

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
