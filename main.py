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

sns.set(style="whitegrid")

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")

    # Ubah kolom tanggal
    df["dteday"] = pd.to_datetime(df["dteday"])

    # Mapping tahun
    year_map = {
        0: "2011",
        1: "2012"
    }

    # Mapping nama bulan
    month_map = {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }

    df["yr_name"] = df["yr"].map(year_map)
    df["mnth_name"] = df["mnth"].map(month_map)

    # Kategori suhu
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
    options=["2011", "2012"]
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
filtered_df = df_main[
    (df_main["yr_name"] == selected_year) &
    (df_main["mnth_name"].isin(selected_months))
].copy()

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
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Penyewaan",
        f"{int(filtered_df['cnt'].sum()):,}"
    )

with col2:
    st.metric(
        "Rata-rata Suhu",
        f"{filtered_df['temp'].mean():.2f}"
    )

with col3:
    st.metric(
        "Rata-rata Kecepatan Angin",
        f"{filtered_df['windspeed'].mean():.2f}"
    )

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

# =====================================================
# TAB 1 — PERBANDINGAN TAHUN
# =====================================================
with tab1:
    st.subheader("📊 Perbandingan Tren Penyewaan 2011 vs 2012")

    yearly_trend = (
        df_main.groupby(["mnth_name", "yr_name"])["cnt"]
        .mean()
        .unstack()
    )

    yearly_trend = yearly_trend.reindex(month_options)

    fig, ax = plt.subplots(figsize=(10, 5))
    yearly_trend.plot(
        marker="o",
        linewidth=2,
        ax=ax
    )

    ax.set_title("Perbandingan Penyewaan Sepeda 2011 vs 2012")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan")

    st.pyplot(fig)

# =====================================================
# TAB 2 — TREN BULANAN
# =====================================================
with tab2:
    st.subheader(f"📈 Tren Bulanan Tahun {selected_year}")

    if not filtered_df.empty:
        actual_order = [
            m for m in month_options if m in selected_months
        ]

        monthly_mean = (
            filtered_df.groupby("mnth_name")["cnt"]
            .mean()
            .reindex(actual_order)
        )

        monthly_total = (
            filtered_df.groupby("mnth_name")["cnt"]
            .sum()
            .reindex(actual_order)
        )

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(
                monthly_mean.index,
                monthly_mean.values,
                marker="o"
            )
            ax.set_title("Rata-rata Penyewaan")
            ax.set_xlabel("Bulan")
            ax.set_ylabel("Jumlah Penyewaan")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(
                monthly_total.index,
                monthly_total.values
            )
            ax.set_title("Total Penyewaan")
            ax.set_xlabel("Bulan")
            ax.set_ylabel("Total Penyewaan")
            st.pyplot(fig)

# =====================================================
# TAB 3 — CASUAL VS REGISTERED
# =====================================================
with tab3:
    st.subheader("👥 Perbandingan Casual vs Registered")

    if not filtered_df.empty:
        actual_order = [
            m for m in month_options if m in selected_months
        ]

        user_analysis = (
            filtered_df.groupby("mnth_name")[["casual", "registered"]]
            .mean()
            .reindex(actual_order)
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(
            user_analysis.index,
            user_analysis["casual"],
            marker="o",
            label="Casual"
        )

        ax.plot(
            user_analysis.index,
            user_analysis["registered"],
            marker="o",
            label="Registered"
        )

        ax.set_title("Casual vs Registered")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Rata-rata Penyewaan")
        ax.legend()

        st.pyplot(fig)

# =====================================================
# TAB 4 — KECEPATAN ANGIN
# =====================================================
with tab4:
    st.subheader("🌬️ Dampak Kecepatan Angin")

    if not filtered_df.empty:
        avg_wind = df_main["windspeed"].mean()

        filtered_df["wind_status"] = filtered_df[
            "windspeed"
        ].apply(
            lambda x: "Tinggi" if x > avg_wind else "Rendah"
        )

        wind_analysis = (
            filtered_df.groupby("wind_status")["cnt"]
            .mean()
            .reindex(["Rendah", "Tinggi"])
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.barplot(
            x=wind_analysis.index,
            y=wind_analysis.values,
            ax=ax
        )

        ax.set_title("Penyewaan Berdasarkan Kecepatan Angin")
        ax.set_ylabel("Rata-rata Penyewaan")

        st.pyplot(fig)

# =====================================================
# TAB 5 — ANALISIS SUHU + KORELASI
# =====================================================
with tab5:
    st.subheader("🔥 Analisis Suhu & Korelasi")

    if not filtered_df.empty:
        actual_order = [
            m for m in month_options if m in selected_months
        ]

        temp_analysis = (
            filtered_df.groupby(
                ["mnth_name", "temp_category"]
            )["cnt"]
            .mean()
            .unstack()
            .reindex(actual_order)
        )

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            temp_analysis.plot(
                kind="bar",
                ax=ax
            )
            ax.set_title("Kategori Suhu")
            ax.set_xlabel("Bulan")
            ax.set_ylabel("Rata-rata Penyewaan")
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))

            corr_matrix = filtered_df[
                ["temp", "atemp", "hum", "windspeed", "cnt"]
            ].corr()

            sns.heatmap(
                corr_matrix,
                annot=True,
                cmap="coolwarm",
                fmt=".2f",
                ax=ax
            )

            ax.set_title("Correlation Matrix")
            st.pyplot(fig)

# =====================================================
# CONCLUSION & RECOMMENDATION (INTERAKTIF)
# =====================================================
st.divider()
st.subheader("Conclusion & Recommendation")

if not filtered_df.empty:
    # Peak month
    peak_month = (
        filtered_df.groupby("mnth_name")["cnt"]
        .sum()
        .idxmax()
    )

    # Average rental
    avg_rental = int(filtered_df["cnt"].mean())

    # Registered vs Casual
    avg_registered = int(filtered_df["registered"].mean())
    avg_casual = int(filtered_df["casual"].mean())

    dominant_user = (
        "Registered"
        if avg_registered > avg_casual
        else "Casual"
    )

    # Wind analysis
    avg_wind = df_main["windspeed"].mean()

    filtered_df["wind_status"] = filtered_df["windspeed"].apply(
        lambda x: "Tinggi" if x > avg_wind else "Rendah"
    )

    wind_analysis = (
        filtered_df.groupby("wind_status")["cnt"]
        .mean()
        .reindex(["Rendah", "Tinggi"])
    )

    if wind_analysis["Rendah"] > wind_analysis["Tinggi"]:
        wind_conclusion = "angin rendah meningkatkan jumlah penyewaan"
    else:
        wind_conclusion = "angin tinggi meningkatkan jumlah penyewaan"

    # Temperature effect
    temp_corr = filtered_df[["temp", "cnt"]].corr().iloc[0, 1]

    if temp_corr > 0:
        temp_conclusion = "suhu memiliki hubungan positif terhadap penyewaan"
    else:
        temp_conclusion = "suhu memiliki hubungan negatif terhadap penyewaan"

    # Layout 2 kolom
    col_conc, col_rec = st.columns(2)

    with col_conc:
        st.markdown("### Conclusion")

        st.write(f"""
        - Pada tahun **{selected_year}**, bulan dengan penyewaan tertinggi terjadi pada **{peak_month}**.
        - Rata-rata penyewaan sepeda mencapai sekitar **{avg_rental} unit**.
        - Pengguna **{dominant_user}** lebih dominan dibanding tipe pengguna lainnya.
        - Kondisi **{wind_conclusion}**.
        - Berdasarkan korelasi data, **{temp_conclusion}**.
        """)

    with col_rec:
        st.markdown("### Recommendation")

        st.write(f"""
        - Fokus penambahan unit sepeda pada bulan **{peak_month}** karena merupakan periode permintaan tertinggi.
        - Pertahankan loyalitas pengguna **{dominant_user}** melalui promo membership dan program retksi.
        - Sesuaikan operasional berdasarkan kondisi cuaca, terutama saat kecepatan angin berubah signifikan.
        - Gunakan strategi promosi musiman pada bulan dengan permintaan rendah untuk meningkatkan penggunaan.
        - Optimalkan layanan pada periode dengan suhu yang mendukung aktivitas bersepeda.
        """)

else:
    st.warning("⚠️ Tidak ada data untuk filter yang dipilih.")

st.caption("Copyright © Charista Septi Dwi Artamy - 2026")