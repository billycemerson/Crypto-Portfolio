# Crypto Portfolio Optimization

Sebuah framework analisis untuk mengoptimalkan portofolio kripto jangka pendek (1–4 minggu) menggunakan pendekatan **GARCH**, **t-Copula**, dan **Markowitz Optimization**.

## 🚀 Fitur Utama

* **GARCH Modeling** – Mengestimasi volatilitas harian aset kripto.
* **t-Copula Simulation** – Menangkap korelasi kompleks antar aset.
* **Markowitz Optimization** – Menentukan bobot optimal dengan mempertimbangkan Sharpe Ratio dan CVaR.
* **Analisis Jangka Pendek** – Fokus pada horizon investasi 1, 2, 3, dan 4 minggu.
* **Kombinasi Portofolio** – Evaluasi semua kombinasi dari 2, 3, dan 4 aset.

## 🗂️ Struktur Proyek

```
Crypto-Portfolio/
├── data/
│   ├── crypto/          # Data mentah kripto
│   ├── prep/            # Data yang telah dipreproses
│   ├── result/          # Hasil analisis (CSV, TXT, grafik)
├── src/
│   ├── data.py          # Mengambil data harga kripto
│   ├── preprocess.py    # Membersihkan dan mempersiapkan data
│   ├── analyze.py       # Script utama untuk analisis & optimasi
├── requirements.txt     # Dependensi Python
└── README.md            # Dokumentasi proyek
```

## 🛠️ Instalasi

```bash
git clone <repository-url>
cd Crypto-Portfolio
pip install -r requirements.txt
```

## 📈 Cara Penggunaan

1. **Ambil data historis kripto:**

```bash
python src/data.py
```

2. **Preproses data:**

```bash
python src/preprocess.py
```

3. **Analisis dan optimasi portofolio:**

```bash
python src/analyze.py
```

## 📁 Output

* Kombinasi portofolio terbaik: `data/result/portfolio_combinations.csv`
* Ringkasan hasil analisis: `data/result/result_analyze.txt`

## 📊 Contoh Hasil

**Portofolio terbaik (2 aset, 1 minggu):**

* Aset: BNB, DOGE
* Bobot: \[0.5, 0.5]
* Sharpe Ratio: 0.0202
* CVaR: 0.3036

**Portofolio terbaik (3 aset, 4 minggu):**

* Aset: ADA, BTC, SOL
* Bobot: \[0.70, 0.01, 0.29]
* Sharpe Ratio: 0.0344
* CVaR: 24.8856

## 🧩 Dependensi

Pastikan Anda telah menginstal:

* `yfinance`
* `pandas`
* `numpy`
* `scipy`
* `arch-py`
* `copulas`

## 📄 Lisensi

Lisensi MIT. Lihat file `LICENSE` untuk informasi selengkapnya.

---
