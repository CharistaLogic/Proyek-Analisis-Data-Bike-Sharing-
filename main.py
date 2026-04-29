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
    df['year_label'] = df['yr'].map({0: '2011', 1: '2012'})
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    df['mnth_name'] = df['mnth'].map(month_map)
    return df

df_all = load_data()

# --- SIDEBAR (FILTERING---
st.sidebar.title("🚲 Filter Analyst")
selected_year = st.sidebar.selectbox("Pilih Tahun:", options=['2011', '2012'], index=1)
month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
selected_months = st.sidebar.multiselect("Pilih Bulan:", options=month_options, default=month_options)

# Eksekusi Filter Utama
filtered_df = df_all[(df_all['year_label'] == selected_year) & (df_all['mnth_name'].isin(selected_months))].copy()

# --- HALAMAN UTAMA ---
st.title("Bike Sharing Analysis Dashboard")
st.markdown(f"**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# Metrik Dinamis
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(f"Total Penyewaan ({selected_year})", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-rata User Registered", f"{filtered_df['registered'].mean():.0f}" if not filtered_df.empty else 0)
with col3:
    st.metric("Rata-rata User Casual", f"{filtered_df['casual'].mean():.0f}" if not filtered_df.empty else 0)

st.divider()

# --- VISUALISASI DATA ---
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
        st.warning("Silakan pilih bulan di sidebar.")

with tab2:
    st.subheader("Pengaruh Kecepatan Angin")
    if not filtered_df.empty:
        avg_wind_val = float(df_all['windspeed'].mean())
        wind_threshold = st.slider("Tentukan Ambang Batas Kecepatan Angin:", 
                                   min_value=float(df_all['windspeed'].min()), 
                                   max_value=float(df_all['windspeed'].max()), 
                                   value=avg_wind_val, step=0.01)

        # Perbaikan label agar konsisten dengan reindex
        filtered_df['wind_status'] = filtered_df['windspeed'].apply(
            lambda x: 'High Wind' if x > wind_threshold else 'Low Wind')
        wind_impact = filtered_df.groupby('wind_status')['cnt'].mean().reindex(['High Wind', 'Low Wind'])
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_impact.index, y=wind_impact.values, palette='viridis', ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan")
        st.pyplot(fig)
        st.write(f"Grafik menunjukkan perbandingan penyewaan berdasarkan ambang batas angin: **{wind_threshold:.2f}**")

# --- CONCLUSION & RECOMMENDATION ---
st.divider()
st.subheader("Conclusion & Recommendation")
with st.expander("Buka untuk melihat Detail Analisis & Rekomendasi"):
    st.write(f"### Analisis Tahun {selected_year} untuk {len(selected_months)} Bulan Terpilih:")
    col_c, col_r = st.columns(2)
    with col_c:
        st.success("**Conclusion**")
        if not filtered_df.empty:
            # Mencari bulan dengan rata-rata penyewaan tertinggi
            max_month = filtered_df.groupby('mnth_name')['cnt'].mean().idxmax()
            avg_cnt = filtered_df['cnt'].mean()
            st.write(f"""
            1. **Tren:** Pada periode {selected_year}, puncak permintaan terjadi di bulan **{max_month}** dengan rata-rata **{avg_cnt:.0f}** penyewaan per hari.
            2. **Kecepatan Angin:** Analisis menunjukkan kondisi angin rendah secara konsisten mendongkrak jumlah penyewaan.
            3. **Tipe Pengguna:** Pengguna Registered tetap menjadi penyumbang volume paling stabil dibandingkan Casual.
            """)

    with col_r:
        st.info("**Recommendation**")
        if not filtered_df.empty:
            rec_type = st.radio("Pilih Fokus Rekomendasi:", ["Operasional", "Marketing"], horizontal=True)
            if rec_type == "Operasional":
                st.write(f"""
                - Segera lakukan penambahan stok dan pengecekan armada pada bulan **{max_month}** karena merupakan puncak permintaan.
                - **Manajemen Cuaca,** Menyesuaikan distribusi sepeda berdasarkan prediksi kecepatan angin harian untuk menjaga kenyamanan pengguna.""")
            else:
                st.write(f"""
                - **Marketing :** Berikan promo pada pengguna Casual untuk meningkatkan konversi ke Registered.
                - **Retensi:** Perkuat program loyalitas bagi pengguna Registered di tahun {selected_year}.""")

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
