import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("day.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])

    # Mapping tambahan
    season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    weather_map = {
        1: "Clear",
        2: "Mist",
        3: "Light Rain/Snow",
        4: "Heavy Rain"
    }

    df["season_name"] = df["season"].map(season_map)
    df["weather_label"] = df["weathersit"].map(weather_map)
    df["day_type"] = df["workingday"].map({0: "Weekend", 1: "Weekday"})
    df["mnth_name"] = df["dteday"].dt.month_name()
    df["year"] = df["dteday"].dt.year

    return df

df = load_data()

# =====================================================
# HEADER
# =====================================================
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis penyewaan sepeda berdasarkan waktu, musim, dan kondisi cuaca")

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.header("🔎 Filter")

selected_year = st.sidebar.selectbox(
    "Pilih Tahun",
    sorted(df["year"].unique())
)

selected_season = st.sidebar.multiselect(
    "Pilih Musim",
    df["season_name"].unique(),
    default=df["season_name"].unique()
)

selected_weather = st.sidebar.multiselect(
    "Pilih Cuaca",
    df["weather_label"].unique(),
    default=df["weather_label"].unique()
)

# Filter data
filtered_df = df[
    (df["year"] == selected_year) &
    (df["season_name"].isin(selected_season)) &
    (df["weather_label"].isin(selected_weather))
]

# =====================================================
# KPI
# =====================================================
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Rentals", f"{int(filtered_df['cnt'].sum()):,}")
col2.metric("Rata-rata Harian", f"{int(filtered_df['cnt'].mean()):,}")
col3.metric("Max Rentals", f"{int(filtered_df['cnt'].max()):,}")

# =====================================================
# TREND
# =====================================================
st.subheader("📈 Trend Peminjaman")

fig, ax = plt.subplots()
sns.lineplot(data=filtered_df, x="dteday", y="cnt", ax=ax)
ax.set_title("Trend Peminjaman Sepeda")

st.pyplot(fig)

st.info("""
Pola menunjukkan fluktuasi dengan kecenderungan musiman.
Permintaan meningkat pada periode tertentu dalam setahun.
""")

# =====================================================
# SEASON ANALYSIS
# =====================================================
st.subheader("🌤️ Analisis Musim")

seasonal = filtered_df.groupby("season_name")["cnt"].mean()

fig, ax = plt.subplots()
sns.barplot(x=seasonal.index, y=seasonal.values, ax=ax)
ax.set_title("Rata-rata Peminjaman per Musim")

st.pyplot(fig)

# =====================================================
# WEATHER ANALYSIS
# =====================================================
st.subheader("🌧️ Analisis Cuaca")

weather = filtered_df.groupby("weather_label")["cnt"].mean()

fig, ax = plt.subplots()
sns.barplot(x=weather.index, y=weather.values, ax=ax)
ax.set_title("Rata-rata Peminjaman Berdasarkan Cuaca")

st.pyplot(fig)

# =====================================================
# DAY TYPE ANALYSIS
# =====================================================
st.subheader("📅 Weekday vs Weekend")

day_type = filtered_df.groupby("day_type")["cnt"].mean()

fig, ax = plt.subplots()
sns.barplot(x=day_type.index, y=day_type.values, ax=ax)
ax.set_title("Perbandingan Peminjaman")

st.pyplot(fig)

# =====================================================
# CONCLUSION & RECOMMENDATION (FIXED STRUCTURE)
# =====================================================
st.divider()
st.subheader("Conclusion & Recommendation")

with st.expander("Klik untuk melihat Detail Analisis & Rekomendasi Strategis"):
    
    if not filtered_df.empty:
        peak_month = filtered_df.groupby("mnth_name")["cnt"].sum().idxmax()
        avg_rental = int(filtered_df["cnt"].mean())
        avg_reg = int(filtered_df["registered"].mean())
        avg_cas = int(filtered_df["casual"].mean())
        dominant_user = "Registered" if avg_reg > avg_cas else "Casual"

        peak_season = filtered_df.groupby("season_name")["cnt"].mean().idxmax()
        best_weather = filtered_df.groupby("weather_label")["cnt"].mean().idxmax()
        dominant_day = filtered_df.groupby("day_type")["cnt"].mean().idxmax()

        col_conc, col_rec = st.columns(2)

        with col_conc:
            st.info("### 📝 Conclusion")
            st.markdown(f"""
            1. **Puncak Permintaan:** Pada periode {selected_year}, bulan **{peak_month}** menjadi yang tertinggi.
            2. **Volume Harian:** Rata-rata mencapai **{avg_rental:,} unit**.
            3. **Pengguna Dominan:** Tipe **{dominant_user}** lebih mendominasi.
            4. **Musim Terbaik:** Aktivitas tertinggi terjadi pada **{peak_season}**.
            5. **Cuaca Optimal:** Kondisi **{best_weather}** paling mendukung.
            6. **Pola Harian:** Aktivitas dominan pada **{dominant_day}**.
            """)

        with col_rec:
            st.success("### 💡 Recommendation")

            rec_focus = st.radio(
                "Pilih Fokus Strategi:",
                ["Manajemen Operasional", "Pemasaran & Pertumbuhan"],
                horizontal=True
            )
            
            if rec_focus == "Manajemen Operasional":
                st.write(f"""
                - Fokus distribusi pada musim **{peak_season}** dan bulan **{peak_month}**
                - Optimalkan operasional saat cuaca **{best_weather}**
                - Tingkatkan ketersediaan pada **{dominant_day}**
                - Prioritaskan layanan untuk pengguna **{dominant_user}**
                """)
            else:
                st.write(f"""
                - Buat promo saat low season
                - Kampanye berbasis cuaca **{best_weather}**
                - Konversi Casual → Registered
                - Tingkatkan loyalitas pengguna **{dominant_user}**
                """)
    else:
        st.warning("⚠️ Data tidak tersedia. Harap sesuaikan filter di sidebar.")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("Bike Sharing Dashboard • Final Version 🚀")
