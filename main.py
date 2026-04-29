import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("data/day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    df["yr"] = df["yr"].map({0:"2011",1:"2012"})
    
    avg_wind = df["windspeed"].mean()
    df["wind_category"] = df["windspeed"].apply(
        lambda x: "High Wind" if x > avg_wind else "Low Wind"
    )
    return df

df = load_data()

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("🔎 Filter")

year = st.sidebar.selectbox("Tahun", df["yr"].unique())

month = st.sidebar.slider(
    "Pilih Rentang Bulan",
    min_value=1,
    max_value=12,
    value=(1,12)
)

filtered = df[
    (df["yr"] == year) &
    (df["mnth"] >= month[0]) &
    (df["mnth"] <= month[1])
]

# ======================
# TITLE
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis penyewaan sepeda berdasarkan waktu & cuaca")

# ======================
# KPI DINAMIS
# ======================
col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", int(filtered["cnt"].sum()))
col2.metric("Rata-rata", int(filtered["cnt"].mean()))
col3.metric("Hari Tertinggi", int(filtered["cnt"].max()))

# ======================
# TOGGLE VISUAL
# ======================
chart_option = st.radio(
    "Pilih Analisis",
    ["Tren Penyewaan", "Pengaruh Angin"]
)

# ======================
# VISUAL 1
# ======================
if chart_option == "Tren Penyewaan":
    st.subheader("📊 Tren Penyewaan Sepeda")

    monthly = filtered.groupby("mnth")["cnt"].mean()

    fig, ax = plt.subplots()
    ax.plot(monthly.index, monthly.values, marker='o')
    ax.set_title("Rata-rata Penyewaan per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.grid()

    st.pyplot(fig)

    st.success("Insight: Penyewaan meningkat di pertengahan tahun → ada pola musiman")

# ======================
# VISUAL 2
# ======================
else:
    st.subheader("🌬️ Pengaruh Kecepatan Angin")

    wind = filtered.groupby("wind_category")["cnt"].mean()

    fig, ax = plt.subplots()
    ax.bar(wind.index, wind.values)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Angin")

    st.pyplot(fig)

    st.warning("Insight: Angin rendah → penyewaan lebih tinggi")

# ======================
# DATA VIEW (INTERAKTIF)
# ======================
with st.expander("📄 Lihat Data"):
    st.dataframe(filtered)
