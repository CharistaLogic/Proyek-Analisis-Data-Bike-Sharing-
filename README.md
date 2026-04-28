# Proyek-Analisis-Data-Bike-Sharing
# Bike Sharing Analysis Dashboard

## Project Overview
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda (Bike Sharing Dataset) guna memahami pola penggunaan berdasarkan waktu, kondisi cuaca, dan tipe pengguna.

Dashboard dibuat menggunakan Streamlit untuk menampilkan hasil analisis secara interaktif.

## Business Questions
1. Bagaimana perbedaan tren rata-rata jumlah penyewaan sepeda (cnt) per bulan antara tahun 2011 dan 2012, serta apa implikasinya terhadap pertumbuhan penggunaan layanan bike sharing?
2. Bagaimana tren rata-rata dan total jumlah penyewaan sepeda (cnt) pada setiap bulan selama tahun 2012, serta bulan mana yang menunjukkan perubahan paling signifikan?
3. Berapa perbedaan rata-rata jumlah penyewaan sepeda (cnt) antara kondisi kecepatan angin di atas rata-rata dan di bawah rata-rata selama tahun 2012, serta bagaimana hasil ini dapat dimanfaatkan untuk strategi operasional berbasis kondisi cuaca?
4. Bagaimana perbandingan rata-rata jumlah penyewaan sepeda antara pengguna casual dan registered pada setiap bulan selama tahun 2012 untuk strategi retensi pelanggan?

## Tools & Libraries
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Dataset
Dataset yang digunakan adalah: day.csv

Dataset berisi informasi harian penyewaan sepeda seperti:
- tanggal
- musim
- suhu
- kelembapan
- kecepatan angin
- jumlah penyewaan
- pengguna casual
- pengguna registered

## Main Insight
- Tahun 2012 memiliki jumlah penyewaan lebih tinggi dibanding 2011
- Peak season terjadi pada pertengahan tahun
- Angin rendah meningkatkan jumlah penyewaan
- Pengguna registered lebih stabil dibanding casual

## Run Dashboard
Jalankan dashboard menggunakan perintah berikut:

```bash id=" "
streamlit run main.py
