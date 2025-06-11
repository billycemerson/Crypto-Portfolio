---

# Crypto Portfolio Optimization

A comprehensive framework to optimize **short-term crypto portfolios** (1–4 weeks) using **GARCH**, **t-Copula**, and **Markowitz Optimization** approaches.

**🔗 Repository:** [github.com/billycemerson/Crypto-Portfolio](https://github.com/billycemerson/Crypto-Portfolio)
**📁 Run from:** `src/` folder

---

## 🚀 Key Features

* **GARCH Modeling** – Estimates daily volatility for each crypto asset.
* **t-Copula Simulation** – Captures complex interdependencies between assets.
* **Markowitz Optimization** – Determines optimal weights considering Sharpe Ratio and CVaR.
* **Short-Term Analysis** – Focused on 1, 2, 3, and 4-week investment horizons.
* **Portfolio Combinations** – Evaluates all combinations of 2, 3, and 4 assets.

---

## 🗂️ Project Structure

```
Crypto-Portfolio/
├── data/
│   ├── crypto/          # Raw crypto data
│   ├── prep/            # Preprocessed data
│   ├── result/          # Output results (CSV, TXT)
├── src/
│   ├── data.py          # Fetch crypto price data
│   ├── preprocess.py    # Clean and prepare the data
│   ├── analyze.py       # Main script for analysis & optimization
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🛠️ Installation

```bash
git clone https://github.com/billycemerson/Crypto-Portfolio.git
cd Crypto-Portfolio
pip install -r requirements.txt
```

---

## 📈 How to Use

1. **Fetch historical crypto data:**

```bash
cd src
python data.py
```

2. **Preprocess the data:**

```bash
python preprocess.py
```

3. **Analyze and optimize the portfolio:**

```bash
python analyze.py
```

---

## 📁 Output

* Best portfolio combinations: `data/result/portfolio_combinations.csv`
* Analysis summary: `data/result/result_analyze.txt`

---

## 📊 Sample Results

**Best Portfolio (2 assets, 1 week):**

* Assets: BNB, DOGE
* Weights: \[0.5, 0.5]
* Sharpe Ratio: 0.0202
* CVaR: 0.3036

**Best Portfolio (3 assets, 4 weeks):**

* Assets: ADA, BTC, SOL
* Weights: \[0.70, 0.01, 0.29]
* Sharpe Ratio: 0.0344
* CVaR: 24.8856

---

## 🧩 Dependencies

Make sure the following packages are installed:

* `yfinance`
* `pandas`
* `numpy`
* `scipy`
* `arch`
* `copulas`

---

## 📄 License

Licensed under the MIT License. See the `LICENSE` file for more details.

---
