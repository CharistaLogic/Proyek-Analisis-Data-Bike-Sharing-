import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 2. Fungsi Memuat Data (Sesuai alur analisis notebook Anda)
@st.cache_data
def load_data():
    # Memuat dataset
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Filter Tahun 2012 (yr=1) sesuai ruang lingkup proyek Anda
    df_2012 = df[df['yr'] == 1].copy()
    
    # Mapping Nama Bulan
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df_2012['mnth_name'] = df_2012['mnth'].map(month_map)
    
    # Kategori Suhu (Sesuai fungsi get_temp_category di notebook)
    def get_temp_category(temp_val):
        if temp_val < 0.33: return 'Cold'
        elif 0.33 <= temp_val < 0.66: return 'Moderate'
        else: return 'Hot'
    df_2012['temp_category'] = df_2012['temp'].apply(get_temp_category)
    
    return df_2012

df_main = load_data()

# --- SIDEBAR (FITUR INTERAKTIF UTAMA) ---
st.sidebar.title("🚲 Opsi Filter")
st.sidebar.markdown("Filter ini akan memanipulasi seluruh grafik dan kesimpulan di dashboard.")

month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_months = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=month_options,
    default=month_options
)

# Terapkan Filter
filtered_df = df_main[df_main['mnth_name'].isin(selected_months)]

# --- HALAMAN UTAMA ---
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# Metrik Interaktif
col1, col2, col3 = st.columns(3)
with col1:
    total_rent = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan", f"{total_rent:,}")
with col2:
    avg_temp = filtered_df['temp'].mean()
    st.metric("Rata-rata Suhu", f"{avg_temp:.2f}")
with col3:
    avg_wind = filtered_df['windspeed'].mean()
    st.metric("Rata-rata Angin", f"{avg_wind:.2f}")

st.divider()

# --- VISUALISASI DATA ---
tab1, tab2, tab3 = st.tabs(["Tren & Tipe User", "Dampak Angin", "Korelasi"])

with tab1:
    st.subheader("Tren Bulanan: Casual vs Registered (2012)")
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
        st.warning("⚠️ Silakan pilih bulan di sidebar.")

with tab2:
    st.subheader("Penyewaan Berdasarkan Kecepatan Angin")
    if not filtered_df.empty:
        # Menghitung status angin berdasarkan rata-rata keseluruhan dataset 2012
        ref_wind = df_main['windspeed'].mean()
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(lambda x: 'Angin Tinggi' if x > ref_wind else 'Angin Rendah')
        wind_impact = filtered_df.groupby('wind_status')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_impact.index, y=wind_impact.values, palette='viridis', ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)

with tab3:
    st.subheader("Matriks Korelasi Variabel Cuaca")
    if not filtered_df.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        corr_matrix = filtered_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        st.pyplot(fig)

# --- BAGIAN INTERAKTIF: CONCLUSION & RECOMMENDATION ---
st.divider()
st.subheader("Conclusion & Recommendation")

# Menggunakan Expander agar interaktif (pengguna perlu klik untuk membaca)
with st.expander("Buka untuk melihat Detail Kesimpulan & Rekomendasi"):
    st.write(f"### Analisis Berdasarkan {len(selected_months)} Bulan Terpilih")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("**Conclusion**")
        # Nilai rata-rata dalam teks ini akan berubah otomatis sesuai filter
        reg_avg = filtered_df['registered'].mean()
        cas_avg = filtered_df['casual'].mean()
        
        st.write(f"""
        1. **Tren Bulanan:** Peningkatan signifikan terjadi di pertengahan tahun, mencapai titik tertinggi pada bulan September.
        2. **Dampak Angin:** Kecepatan angin rendah terbukti lebih mendukung volume penyewaan yang lebih besar dibanding angin tinggi.
        3. **Pola Pengguna:** Pengguna Registered ({reg_avg:.0f} rata-rata) jauh lebih stabil dan dominan dibandingkan pengguna Casual ({cas_avg:.0f} rata-rata).
        """)

    with col_b:
        st.info("**Recommendation Action Item**")
        st.write("""
        1. **Manajemen Inventori:** Menambah stok sepeda di bulan Mei-September karena permintaan berada di level tertinggi.
        2. **Operasional:** Menyesuaikan distribusi unit saat perkiraan cuaca menunjukkan kondisi angin rendah.
        3. **Program Retensi:** Memberikan insentif khusus bagi pengguna *Registered* agar pola penggunaan tetap stabil sepanjang tahun.
        4. **Pemasaran:** Menargetkan promosi bagi pengguna *Casual* pada bulan-bulan dengan suhu hangat.
        """)

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
