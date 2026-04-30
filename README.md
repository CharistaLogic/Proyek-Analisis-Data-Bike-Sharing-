# Proyek Bike Sharing Analysis Dashboard

## Project Overview
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda (Bike Sharing Dataset) guna memahami pola penggunaan berdasarkan waktu dan tipe pengguna.
Dashboard dibuat menggunakan Streamlit untuk menampilkan hasil analisis secara interaktif

Dashboard dibuat menggunakan Streamlit untuk menampilkan hasil analisis secara interaktif.
## Business Questions
1. Bagaimana perbedaan tren rata rata jumlah penyewa sepeda perbulan antara tahun 2011 dan 2012?
2. Bagaimana perbandingan rata-rata jumlah penyewaan sepeda antara pengguna casual dan registered pada setiap bulan selama tahun 2012?

## Tools & Libraries
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Dataset
Dataset yang digunakan adalah: **day.csv**, yang berisi informasi harian penyewaan sepeda seperti:
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

## Setup Evironment
Pastikan Python sudah terinstall di perangkat Anda.
Bisa menggunakan : 
- Python 3.10 atau 3.11
- 
Cek versi Python:
- python --version

## Membuat virtual Environment
python -m venv venv
## Mengaktifkan virtual Environment
python -m venv venv

## Instalasi Dependencies
Install semua library yang dibutuhkan:

pip install pandas matplotlib seaborn streamlit

## Menjalankan Dashboard Streamlit
Setelah semua dependency terinstall, jalankan dashboard dengan perintah: 
 
 streamlit run dashboard/main.py

## Akses Dashboard
Setelah dijalankan, dashboard akan otomatis terbuka di browser:
http://localhost:8501

## Cara Deploy
Dashboard dapat di-deploy menggunakan Streamlit Cloud:
1. Upload project ke GitHub
2. Buka https://streamlit.io/cloud
3. Klik New App
4. Pilih repository
5. Pilih file utama: main.py
6. Klik Deploy

