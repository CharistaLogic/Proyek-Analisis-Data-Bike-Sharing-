import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 2. Fungsi Memuat Data (Sesuai alur analisis Notebook Anda)
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Mapping Nama Bulan & Tahun agar dashboard lebih mudah digunakan
    df['year_label'] = df['yr'].map({0: '2011', 1: '2012'})
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df['mnth_name'] = df['mnth'].map(month_map)
    
    return df

df_all = load_data()

# --- SIDEBAR (FITUR INTERAKTIF: FILTERING) ---
st.sidebar.title("🚲 Opsi Filter")
st.sidebar.markdown("Manipulasi data di bawah ini untuk melihat perubahan pada grafik dan kesimpulan secara real-time.")

# Filter Tahun
selected_year = st.sidebar.selectbox("Pilih Tahun:", options=['2011', '2012'], index=1)

# Filter Bulan (Fitur interaktif utama untuk eksplorasi)
month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_months = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=month_options,
    default=month_options
)

# Eksekusi Filter
filtered_df = df_all[(df_all['year_label'] == selected_year) & (df_all['mnth_name'].isin(selected_months))]

# --- HALAMAN UTAMA ---
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# Metrik Utama (Dinamis merespons filter)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"Total Penyewaan ({selected_year})", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata Registered", f"{filtered_df['registered'].mean():.0f}" if not filtered_df.empty else 0)
with col3:
    st.metric("Rata-rata Casual", f"{filtered_df['casual'].mean():.0f}" if not filtered_df.empty else 0)

st.divider()

# --- VISUALISASI DATA (2 Pertanyaan Bisnis Utama) ---
tab1, tab2 = st.tabs(["Tren & Tipe Pengguna", "Pengaruh Kecepatan Angin"])

with tab1:
    st.subheader(f"Tren Rata-rata Penyewaan per Bulan ({selected_year})")
    if not filtered_df.empty:
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
        st.warning("Silakan pilih minimal satu bulan di sidebar.")

with tab2:
    st.subheader("Penyewaan Berdasarkan Kecepatan Angin")
    if not filtered_df.empty:
        # Menghitung status angin berdasarkan rata-rata tahun terpilih
        ref_wind = filtered_df['windspeed'].mean()
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(lambda x: 'Angin Tinggi' if x > ref_wind else 'Angin Rendah')
        wind_impact = filtered_df.groupby('wind_status')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_impact.index, y=wind_impact.values, palette='viridis', ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)

# --- BAGIAN INTERAKTIF: CONCLUSION & RECOMMENDATION ---
st.divider()
st.subheader("Conclusion & Recommendation")

# Fitur Interaktif: Expander (User harus klik untuk membaca)
with st.expander("Buka untuk melihat Detail Analisis & Rekomendasi"):
    st.write(f"### Analisis Tahun {selected_year} untuk {len(selected_months)} Bulan Terpilih:")
    
    col_c, col_r = st.columns(2)
    with col_c:
        st.success("**Conclusion**")
        # Logika Dinamis: Angka dan teks berubah otomatis mengikuti filter
        if not filtered_df.empty:
            max_month = filtered_df.groupby('mnth_name')['cnt'].mean().idxmax()
            avg_cnt = filtered_df['cnt'].mean()
            st.write(f"""
            1. **Tren:** Pada periode terpilih, puncak permintaan terjadi di bulan **{max_month}** dengan rata-rata **{avg_cnt:.0f}** penyewaan per hari.
            2. **Kecepatan Angin:** Analisis menunjukkan bahwa kondisi angin rendah secara konsisten mendongkrak jumlah penyewaan.
            3. **Tipe Pengguna:** Pengguna Registered tetap menjadi penyumbang volume penyewaan yang paling stabil dibandingkan Casual.
            """)
        else:
            st.write("Silakan pilih data pada sidebar untuk melihat kesimpulan.")

    with col_r:
        st.info("**Recommendation Action**")
        st.write("""
        - **Optimalisasi:** Menambah jumlah unit sepeda pada bulan dengan permintaan tertinggi (Mei-September).
        - **Operasional:** Mengatur distribusi armada berdasarkan prediksi cuaca dan kondisi angin.
        - **Strategi Marketing:** Mengembangkan promo khusus untuk pengguna Casual guna meningkatkan konversi menjadi Registered.
        """)

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
