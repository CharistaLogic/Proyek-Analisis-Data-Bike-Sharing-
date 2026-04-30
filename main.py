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
    try:
        df = pd.read_csv("day.csv")
    except FileNotFoundError:
        st.error("File 'day.csv' tidak ditemukan.")
        return pd.DataFrame()

    df["dteday"] = pd.to_datetime(df["dteday"])

    year_map = {0: "2011", 1: "2012"}
    month_map = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    df["yr_name"] = df["yr"].map(year_map)
    df["mnth_name"] = df["mnth"].map(month_map)

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
# SIDEBAR
# =====================================================
st.sidebar.title("Filter Analisis")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun:",
    options=["2011", "2012"],
    index=1
)

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
# FILTER DATA (FIXED)
# =====================================================
filtered_df = df_main[
    (df_main["yr_name"] == selected_year) &
    (df_main["mnth_name"].isin(selected_months))
].copy()

# FIX: threshold dinamis + tidak duplikasi
if not filtered_df.empty:
    threshold_wind = filtered_df["windspeed"].mean()
    filtered_df["wind_status"] = filtered_df["windspeed"].apply(
        lambda x: "Tinggi" if x > threshold_wind else "Rendah"
    )
else:
    threshold_wind = 0

# =====================================================
# HEADER
# =====================================================
st.title("Dashboard Analisis Penyewaan Sepeda")
st.markdown("**Nama:** Charista Septi Dwi Artamy | **ID Dicoding:** CDCC183D6X2720")

# =====================================================
# EMPTY HANDLING (UX FIX)
# =====================================================
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data sesuai filter.")
    st.info("Silakan pilih bulan lain atau ubah tahun.")
    st.stop()

# =====================================================
# METRIC
# =====================================================
col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", f"{int(filtered_df['cnt'].sum()):,}")
col2.metric("Rata-rata Suhu", f"{filtered_df['temp'].mean():.2f}")
col3.metric("Rata-rata Kecepatan Angin", f"{filtered_df['windspeed'].mean():.2f}")

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

# TAB 1 (GLOBAL - FIX: kasih keterangan)
with tab1:
    st.subheader("Perbandingan Tren Penyewaan 2011 vs 2012")
    st.caption("Visualisasi ini menggunakan seluruh data (tidak terpengaruh filter).")

    yearly_trend = df_main.groupby(["mnth_name", "yr_name"])["cnt"].mean().unstack()
    yearly_trend = yearly_trend.reindex(month_options)

    fig, ax = plt.subplots(figsize=(10, 5))
    yearly_trend.plot(marker="o", linewidth=2, ax=ax)
    st.pyplot(fig)

# TAB 2
with tab2:
    st.subheader(f"Tren Bulanan Tahun {selected_year}")

    actual_order = [m for m in month_options if m in selected_months]

    monthly_mean = filtered_df.groupby("mnth_name")["cnt"].mean().reindex(actual_order)
    monthly_total = filtered_df.groupby("mnth_name")["cnt"].sum().reindex(actual_order)

    col_a, col_b = st.columns(2)

    with col_a:
        fig, ax = plt.subplots()
        ax.plot(monthly_mean.index, monthly_mean.values, marker="o")
        st.pyplot(fig)

    with col_b:
        fig, ax = plt.subplots()
        ax.bar(monthly_total.index, monthly_total.values)
        st.pyplot(fig)

# TAB 3
with tab3:
    st.subheader("Analisis Tipe Pengguna")

    actual_order = [m for m in month_options if m in selected_months]

    user_analysis = filtered_df.groupby("mnth_name")[["casual", "registered"]].mean().reindex(actual_order)

    fig, ax = plt.subplots()
    ax.plot(user_analysis.index, user_analysis["casual"], marker="o", label="Casual")
    ax.plot(user_analysis.index, user_analysis["registered"], marker="o", label="Registered")
    ax.legend()
    st.pyplot(fig)

# TAB 4 (FIX TOTAL)
with tab4:
    st.subheader("Dampak Kecepatan Angin")

    wind_analysis = filtered_df.groupby("wind_status")["cnt"].mean().reindex(["Rendah", "Tinggi"])

    fig, ax = plt.subplots()
    sns.barplot(x=wind_analysis.index, y=wind_analysis.values, ax=ax)
    st.pyplot(fig)

    st.caption(f"Ambang batas kecepatan angin (dinamis): {threshold_wind:.2f}")

# TAB 5
with tab5:
    st.subheader("Analisis Suhu & Korelasi")

    col_x, col_y = st.columns(2)

    with col_x:
        actual_order = [m for m in month_options if m in selected_months]
        temp_analysis = filtered_df.groupby(["mnth_name", "temp_category"])["cnt"].mean().unstack().reindex(actual_order)

        fig, ax = plt.subplots()
        temp_analysis.plot(kind="bar", ax=ax)
        st.pyplot(fig)

    with col_y:
        fig, ax = plt.subplots()
        corr = filtered_df[["temp", "atemp", "hum", "windspeed", "cnt"]].corr()
        sns.heatmap(corr, annot=True, ax=ax)
        st.pyplot(fig)

# =====================================================
# CONCLUSION (TIDAK DIUBAH)
# =====================================================
st.divider()
st.subheader("Conclusion & Recommendation")

with st.expander("Klik untuk melihat Detail Analisis & Rekomendasi Strategis"):
    peak_month = filtered_df.groupby("mnth_name")["cnt"].sum().idxmax()
    avg_rental = int(filtered_df["cnt"].mean())
    avg_reg = int(filtered_df["registered"].mean())
    avg_cas = int(filtered_df["casual"].mean())
    dominant_user = "Registered" if avg_reg > avg_cas else "Casual"

    wind_analysis = filtered_df.groupby("wind_status")["cnt"].mean()
    wind_res = "rendah meningkatkan minat penyewaan" if wind_analysis.get("Rendah", 0) > wind_analysis.get("Tinggi", 0) else "tinggi meningkatkan minat penyewaan"

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"""
        1. Puncak pada bulan {peak_month}
        2. Rata-rata {avg_rental}
        3. Dominan {dominant_user}
        4. Angin {wind_res}
        """)

    with col2:
        st.success("Strategi disesuaikan dengan kondisi data")

st.caption("Copyright © 2026")
