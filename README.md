Crypto Portfolio Optimization

This project uses **GARCH-Copula Markowitz** methodology to find the optimal portfolio of 10 cryptocurrencies for short-term investments (1-4 weeks). The analysis generates combinations of 2, 3, and 4 assets, evaluating their performance based on metrics like Sharpe Ratio and Conditional Value at Risk (CVaR).

Features
- GARCH Model: Models the volatility of individual cryptocurrencies.
- Copula Simulation: Simulates multivariate returns using a t-Copula.
- Markowitz Optimization: Finds the optimal portfolio weights for maximizing Sharpe Ratio while minimizing risk.
- Short-Term Horizons: Analyzes investment periods of 1, 2, 3, and 4 weeks.
- Portfolio Combinations: Evaluates combinations of 2, 3, and 4 assets.

Project Structure
Crypto-Portfolio/
├── data/
│   ├── crypto/          # Raw cryptocurrency data
│   ├── prep/            # Preprocessed data
│   ├── result/          # Analysis results (CSV, TXT)
├── src/
│   ├── data.py          # Script to fetch cryptocurrency data
│   ├── preprocess.py    # Script to preprocess data
│   ├── analyze.py       # Main analysis script
├── requirements.txt     # Python dependencies
└── README.txt           # Project documentation

Installation

1. Clone the repository:
   git clone <repository-url>
   cd Crypto-Portfolio

2. Install the required Python packages:
   pip install -r requirements.txt

Usage

Step 1: Fetch Cryptocurrency Data
Run the data.py script to download historical cryptocurrency data:
python src/data.py

Step 2: Preprocess the Data
Run the preprocess.py script to clean and prepare the data:
python src/preprocess.py

Step 3: Analyze and Optimize Portfolios
Run the analyze.py script to perform portfolio optimization:
python src/analyze.py

Outputs
- Portfolio Combinations: Saved in data/result/portfolio_combinations.csv.
- Analysis Summary: Saved in data/result/result_analyze.txt.

Example Results
- Best Portfolio for 2 assets (1_week):
  - Assets: BNB, DOGE
  - Weights: [0.5, 0.5]
  - Sharpe Ratio: 0.0202
  - CVaR: 0.3036

- Best Portfolio for 3 assets (4_week):
  - Assets: ADA, BTC, SOL
  - Weights: [0.7, 0.01, 0.29]
  - Sharpe Ratio: 0.0344
  - CVaR: 24.8856

Dependencies
The project requires the following Python libraries:
- yfinance
- pandas
- numpy
- scipy
- arch-py
- copulas

Install them using the requirements.txt file.

License
This project is licensed under the MIT License. See the LICENSE file for details.
