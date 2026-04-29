import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])

    # Mapping tahun
    df["yr"] = df["yr"].map({0: "2011", 1: "2012"})

    # Kategori angin (sesuai notebook)
    avg_wind = df["windspeed"].mean()
    df["wind_category"] = df["windspeed"].apply(
        lambda x: "High Wind" if x > avg_wind else "Low Wind"
    )

    return df

df = load_data()

# ======================
# SIDEBAR (INTERAKTIF)
# ======================
st.sidebar.header("🔎 Filter Data")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    sorted(df["yr"].unique())
)

selected_month = st.sidebar.multiselect(
    "Pilih Bulan",
    sorted(df["mnth"].unique()),
    default=sorted(df["mnth"].unique())
)

filtered_df = df[
    (df["yr"] == selected_year) &
    (df["mnth"].isin(selected_month))
]

# ======================
# TITLE
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan waktu dan kondisi cuaca")

# ======================
# KPI
# ======================
col1, col2 = st.columns(2)

col1.metric("Total Penyewaan", int(filtered_df["cnt"].sum()))
col2.metric("Rata-rata Harian", int(filtered_df["cnt"].mean()))

# ======================
# 📊 VISUAL 1 (PERTANYAAN BISNIS)
# Tren penyewaan per bulan
# ======================
st.subheader("📊 Tren Penyewaan Sepeda per Bulan")

monthly = filtered_df.groupby("mnth")["cnt"].mean()

fig1, ax1 = plt.subplots()
ax1.plot(monthly.index, monthly.values, marker='o')
ax1.set_title("Rata-rata Penyewaan per Bulan")
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Jumlah Penyewaan")
ax1.grid()

st.pyplot(fig1)

st.markdown("""
**Insight:**  
Terjadi peningkatan penyewaan pada pertengahan tahun, menunjukkan adanya pola musiman (seasonality) pada penggunaan sepeda.
""")

# ======================
# 📊 VISUAL 2 (PERTANYAAN BISNIS)
# Pengaruh kecepatan angin
# ======================
st.subheader("🌬️ Pengaruh Kecepatan Angin")

wind = filtered_df.groupby("wind_category")["cnt"].mean()

fig2, ax2 = plt.subplots()
ax2.bar(wind.index, wind.values)
ax2.set_title("Rata-rata Penyewaan Berdasarkan Angin")
ax2.set_xlabel("Kategori Angin")
ax2.set_ylabel("Jumlah Penyewaan")

st.pyplot(fig2)

st.markdown("""
**Insight:**  
Penyewaan sepeda lebih tinggi pada kondisi angin rendah, menunjukkan bahwa faktor kenyamanan lingkungan memengaruhi penggunaan layanan.
""")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("© 2026 Bike Sharing Dashboard")
