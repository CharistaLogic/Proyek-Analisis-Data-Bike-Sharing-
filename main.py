import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])

    # Mapping tahun
    df["yr"] = df["yr"].map({0: "2011", 1: "2012"})

    # Kategori wind (sesuai notebook)
    avg_wind = df["windspeed"].mean()
    df["wind_category"] = df["windspeed"].apply(
        lambda x: "High Wind" if x > avg_wind else "Low Wind"
    )

    return df

df = load_data()

# ======================
# FILTER (INTERAKTIF)
# ======================
st.sidebar.header("🔎 Filter")

selected_month = st.sidebar.multiselect(
    "Pilih Bulan",
    sorted(df["mnth"].unique()),
    default=sorted(df["mnth"].unique())
)

# Fokus analisis ke 2012 (sesuai notebook)
df_2012 = df[df["yr"] == "2012"]

filtered_df = df_2012[df_2012["mnth"].isin(selected_month)]

# ======================
# TITLE
# ======================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan waktu dan kondisi angin (tahun 2012)")

# ======================
# 📊 VISUAL 1
# Tren penyewaan (Pertanyaan Bisnis 1)
# ======================
st.subheader("📊 Tren Penyewaan Sepeda per Bulan (2012)")

monthly = filtered_df.groupby("mnth")["cnt"].mean()

fig1, ax1 = plt.subplots()
ax1.plot(monthly.index, monthly.values, marker='o')
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Rata-rata Penyewaan")
ax1.set_title("Tren Penyewaan Sepeda")
ax1.grid()

st.pyplot(fig1)

st.markdown("""
**Insight:**  
Terjadi peningkatan penyewaan pada pertengahan tahun, menunjukkan adanya pola musiman (seasonality).
""")

# ======================
# 📊 VISUAL 2
# Pengaruh angin (Pertanyaan Bisnis 2)
# ======================
st.subheader("🌬️ Pengaruh Kecepatan Angin terhadap Penyewaan")

wind = filtered_df.groupby("wind_category")["cnt"].mean()

fig2, ax2 = plt.subplots()
ax2.bar(wind.index, wind.values)
ax2.set_xlabel("Kategori Angin")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_title("Pengaruh Kecepatan Angin")

st.pyplot(fig2)

st.markdown("""
**Insight:**  
Penyewaan sepeda lebih tinggi pada kondisi angin rendah, menunjukkan faktor kenyamanan memengaruhi penggunaan layanan.
""")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.caption("Dashboard Analisis Bike Sharing - 2012")
