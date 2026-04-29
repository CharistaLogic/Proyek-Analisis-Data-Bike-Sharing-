# Proyek Bike Sharing Analysis Dashboard

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

## Setup Evironment
Pastikan Python sudah terinstall di perangkat Anda.
Bisa menggunakan : 
- Python 3.10 atau 3.11
Cek versi Python:
python --version

## Instalasi Dependencies
Install semua library yang dibutuhkan:

pip install pandas matplotlib seaborn streamlit

##Struktur Folder Proyek
Pastikan struktur folder seperti berikut:
project/
│
├── data/
│   └── day.csv
│
├── app.py
│
├── notebook.ipynb
│
└── README.md

## Cara Deploy
Dashboard dapat di-deploy menggunakan Streamlit Cloud:
1. Upload project ke GitHub
2. Buka https://streamlit.io/cloud
3. Pilih repository
4. Jalankan app.py

## Menjalankan Dashboard Streamlit
Setelah semua dependency terinstall, jalankan dashboard dengan perintah: 
 streamlit run main.py

## Akses Dashboard
Setelah dijalankan, dashboard akan otomatis terbuka di browser:
http://localhost:8501

## Cara Deploy
Dashboard dapat di-deploy menggunakan Streamlit Cloud:
1. Upload project ke GitHub
2. Buka https://streamlit.io/cloud
3. Pilih repository
4. Jalankan app.py

