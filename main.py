import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    layout="wide"
)

# Set style seaborn agar visualisasi konsisten
sns.set(style="whitegrid")

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    # Gunakan penanganan error jika file tidak ditemukan
    try:
        df = pd.read_csv("day.csv")
    except FileNotFoundError:
        st.error("File 'day.csv' tidak ditemukan. Pastikan file ada di direktori yang sama.")
        return pd.DataFrame()

    # Data Wrangling: Pastikan kolom tanggal benar-benar bertipe datetime
    df["dteday"] = pd.to_datetime(df["dteday"])

    # Mapping tahun dan bulan agar filter lebih "manusiawi"
    year_map = {0: "2011", 1: "2012"}
    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    df["yr_name"] = df["yr"].map(year_map)
    df["mnth_name"] = df["mnth"].map(month_map)

    # Menambahkan kategori suhu untuk tab analisis suhu
    def get_temp_category(temp_val):
        if temp_val < 0.33:
            return "Cold"
        elif temp_val < 0.66:
            return "Moderate"
        else:
            return "Hot"

    df["temp_category"] = df["temp"].apply(get_temp_category)

    return df

df_main = load_data()

# =====================================================
# SIDEBAR FILTER
# =====================================================
st.sidebar.title("Filter Analisis")

# Filter Tahun
selected_year = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=["2011", "2012"],
    index=1 # Default ke 2012
)

# Filter Bulan
month_options = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

selected_months = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=month_options,
    default=month_options
)

# =====================================================
# FILTER DATA
# =====================================================
# Menambahkan .copy() untuk menghindari SettingWithCopyWarning
filtered_df = df_main[
    (df_main["yr_name"] == selected_year) &
    (df_main["mnth_name"].isin(selected_months))
].copy()

threshold_wind = df_main["windspeed"].mean()
filtered_df["wind_status"] = filtered_df["windspeed"].apply(
    lambda x: "Tinggi" if x > threshold_wind else "Rendah"
)

# =====================================================
# HEADER
# =====================================================
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown(
    "**Nama:** Charista Septi Dwi Artamy | "
    "**ID Dicoding:** CDCC183D6X2720"
)

# =====================================================
# METRIC CARDS
# =====================================================
if not filtered_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Penyewaan", f"{int(filtered_df['cnt'].sum()):,}")
    with col2:
        st.metric("Rata-rata Suhu", f"{filtered_df['temp'].mean():.2f}")
    with col3:
        st.metric("Rata-rata Kecepatan Angin", f"{filtered_df['windspeed'].mean():.2f}")
else:
    st.warning("⚠️ Silakan pilih setidaknya satu bulan pada filter.")

st.divider()

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Perbandingan Tahun",
    "Tren Bulanan",
    "Casual vs Registered",
    "Kecepatan Angin",
    "Analisis Suhu"
])

# 1. PERBANDINGAN TAHUN (Global View)
with tab1:
    st.subheader("Perbandingan Tren Penyewaan 2011 vs 2012")
    yearly_trend = df_main.groupby(["mnth_name", "yr_name"])["cnt"].mean().unstack()
    yearly_trend = yearly_trend.reindex(month_options)

    fig, ax = plt.subplots(figsize=(10, 5))
    yearly_trend.plot(marker="o", linewidth=2, ax=ax, color=['#FF9999', '#66B2FF'])
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

# 2. TREN BULANAN (Sesuai Filter)
with tab2:
    st.subheader(f"Tren Bulanan Tahun {selected_year}")
    if not filtered_df.empty:
        actual_order = [m for m in month_options if m in selected_months]
        monthly_mean = filtered_df.groupby("mnth_name")["cnt"].mean().reindex(actual_order)
        monthly_total = filtered_df.groupby("mnth_name")["cnt"].sum().reindex(actual_order)

        col_a, col_b = st.columns(2)
        with col_a:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(monthly_mean.index, monthly_mean.values, marker="o", color='#2E7D32')
            ax.set_title("Rata-rata Penyewaan per Hari")
            st.pyplot(fig)
        with col_b:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(monthly_total.index, monthly_total.values, color='#81C784')
            ax.set_title("Total Penyewaan per Bulan")
            st.pyplot(fig)

# 3. CASUAL VS REGISTERED
with tab3:
    st.subheader("Analisis Tipe Pengguna: Casual vs Registered")
    if not filtered_df.empty:
        actual_order = [m for m in month_options if m in selected_months]
        user_analysis = filtered_df.groupby("mnth_name")[["casual", "registered"]].mean().reindex(actual_order)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(user_analysis.index, user_analysis["casual"], marker="o", label="Casual", color='#FF7043')
        ax.plot(user_analysis.index, user_analysis["registered"], marker="o", label="Registered", color='#1976D2')
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.legend()
        st.pyplot(fig)

# 4. KECEPATAN ANGIN
with tab4:
    st.subheader("Dampak Kecepatan Angin Terhadap Penyewaan")
    if not filtered_df.empty:
        # Menggunakan rata-rata seluruh data sebagai ambang batas tetap
        threshold_wind = df_main["windspeed"].mean()
        filtered_df["wind_status"] = filtered_df["windspeed"].apply(lambda x: "Tinggi" if x > threshold_wind else "Rendah")
        
        wind_analysis = filtered_df.groupby("wind_status")["cnt"].mean().reindex(["Rendah", "Tinggi"])

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=wind_analysis.index, y=wind_analysis.values, palette=['#4CAF50', '#E53935'], ax=ax)
        ax.set_ylabel("Rata-rata Penyewaan harian")
        st.pyplot(fig)
        st.write(f"Keterangan: Ambang batas kecepatan angin adalah **{threshold_wind:.2f}** (rata-rata keseluruhan).")

# 5. ANALISIS SUHU & KORELASI
with tab5:
    st.subheader("Analisis Korelasi & Faktor Lingkungan")
    if not filtered_df.empty:
        col_x, col_y = st.columns(2)
        with col_x:
            actual_order = [m for m in month_options if m in selected_months]
            temp_analysis = filtered_df.groupby(["mnth_name", "temp_category"])["cnt"].mean().unstack().reindex(actual_order)
            fig, ax = plt.subplots(figsize=(8, 5))
            temp_analysis.plot(kind="bar", ax=ax, cmap='viridis')
            ax.set_title("Rata-rata Penyewaan per Kategori Suhu")
            st.pyplot(fig)
        with col_y:
            fig, ax = plt.subplots(figsize=(8, 5))
            corr_matrix = filtered_df[["temp", "atemp", "hum", "windspeed", "cnt"]].corr()
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Heatmap Korelasi Variabel")
            st.pyplot(fig)
# =====================================================
# CONCLUSION & RECOMMENDATION (VERSI INTERAKTIF)
# =====================================================
st.divider()
st.subheader("Conclusion & Recommendation")

# Menggunakan Expander agar tampilan lebih bersih
with st.expander("Klik untuk melihat Detail Analisis & Rekomendasi Strategis"):
    
    # Logic perhitungan otomatis berdasarkan filter yang dipilih user
    if not filtered_df.empty:
        peak_month = filtered_df.groupby("mnth_name")["cnt"].sum().idxmax()
        avg_rental = int(filtered_df["cnt"].mean())
        avg_reg = int(filtered_df["registered"].mean())
        avg_cas = int(filtered_df["casual"].mean())
        dominant_user = "Registered" if avg_reg > avg_cas else "Casual"
        
        # Penentuan korelasi angin secara otomatis
        wind_analysis = filtered_df.groupby("wind_status")["cnt"].mean()
        wind_res = "rendah meningkatkan minat penyewaan" if wind_analysis.get("Rendah", 0) > wind_analysis.get("Tinggi", 0) else "tinggi meningkatkan minat penyewaan"

        # Layout kolom untuk memisahkan Kesimpulan dan Rekomendasi
        col_conc, col_rec = st.columns(2)

        with col_conc:
            st.info("###Conclusion")
            st.markdown(f"""
            1. **Puncak Permintaan:** Pada periode {selected_year}, bulan **{peak_month}** menjadi periode dengan aktivitas penyewaan tertinggi.
            2. **Volume Harian:** Rata-rata penyewaan mencapai **{avg_rental:,} unit** per hari di bawah filter yang dipilih.
            3. **Profil Pengguna:** Tipe pengguna **{dominant_user}** mendominasi pasar, menunjukkan basis pelanggan yang kuat.
            4. **Faktor Cuaca:** Terbukti bahwa kondisi **{wind_res}**, sesuai dengan hasil visualisasi pada tab sebelumnya.
            """)

        with col_rec:
            st.success("###Recommendation")
            # FITUR INTERAKTIF: User bisa memilih fokus rekomendasi
            rec_focus = st.radio(
                "Pilih Fokus Strategi:",
                ["Manajemen Operasional", "Pemasaran & Pertumbuhan"],
                horizontal=True
            )
            
            if rec_focus == "Manajemen Operasional":
                st.write(f"""
                - **Alokasi Armada:** Menambah stok sepeda di titik-titik ramai pada bulan **{peak_month}**.
                - **Mitigasi Cuaca:** Menyiapkan protokol pemeliharaan saat kecepatan angin masuk kategori 'Tinggi'.
                - **Stabilitas:** Memastikan ketersediaan bagi pengguna **{dominant_user}** tetap terjaga di jam sibuk.
                """)
            else:
                st.write(f"""
                - **Kampanye Musiman:** Meluncurkan promo khusus pada bulan dengan permintaan rendah untuk menyeimbangkan okupansi.
                - **Konversi Pengguna:** Mengajak pengguna Casual beralih ke Registered melalui diskon membership pada hari-hari dengan cuaca mendukung.
                - **Loyalitas:** Memberikan reward eksklusif bagi pengguna **{dominant_user}** untuk mempertahankan retensi.
                """)
    else:
        st.warning("⚠️ Data tidak tersedia. Harap sesuaikan filter di sidebar.")
        
st.caption("Copyright © Charista Septi Dwi Artamy - 2026")
