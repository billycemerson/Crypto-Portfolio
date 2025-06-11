import numpy as np
import pandas as pd
from arch import arch_model
from scipy.stats import multivariate_t
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf
import matplotlib.pyplot as plt
import itertools
import os

# Configuration
data_dir = "../data/prep/"
result_dir = "../data/result/"
result_file = os.path.join(result_dir, "result_analyze.txt")
csv_file = os.path.join(result_dir, "portfolio_combinations.csv")
fig_file = os.path.join(result_dir, "sharpe_vs_cvar.png")
horizons = {'1_week': 7, '2_week': 14, '3_week': 21, '4_week': 28}
n_simulations = 1000
risk_free_rate = 0.04
adjusted_rf = (1 + risk_free_rate) ** (28 / 365) - 1
min_weight = 0.01
max_weight = 0.70

def load_data():
    dfs, crypto_symbols = [], []
    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            symbol = file.split(".")[0]
            crypto_symbols.append(symbol)
            df = pd.read_csv(os.path.join(data_dir, file), parse_dates=['Date'], index_col='Date')
            df.rename(columns={'Daily Return': symbol}, inplace=True)
            dfs.append(df[symbol])
    combined = pd.concat(dfs, axis=1)
    combined = combined[(combined.index >= "2024-01-02") & (combined.index <= "2025-05-31")]
    return combined.dropna(), crypto_symbols

def fit_garch(series):
    model = arch_model(series * 100, vol='Garch', p=1, q=1, dist='normal')
    return model.fit(update_freq=0, disp='off')

def estimate_df_mle(residuals):
    def neg_log_likelihood(df):
        if df <= 2: return 1e10
        return -np.sum(multivariate_t.logpdf(residuals, df=df, loc=np.zeros(residuals.shape[1]), shape=np.cov(residuals.T)))
    result = minimize(neg_log_likelihood, x0=np.array([5]), bounds=[(2.01, 30)])
    return result.x[0]

def simulate_returns(horizon_days, garch_results, corr_matrix, crypto_symbols, df):
    sim_residuals = multivariate_t.rvs(loc=np.zeros(len(crypto_symbols)), shape=corr_matrix, df=df,
                                       size=horizon_days * n_simulations).reshape(n_simulations, horizon_days, len(crypto_symbols))
    sim_returns = np.zeros((n_simulations, horizon_days, len(crypto_symbols)))

    for i, symbol in enumerate(crypto_symbols):
        model = garch_results[symbol]
        omega = model.params['omega'] / 10000
        alpha = model.params['alpha[1]']
        beta = model.params['beta[1]']
        last_sigma = model.conditional_volatility.iloc[-1] / 100
        last_resid = model.resid.iloc[-1] / 100

        for sim in range(n_simulations):
            sigma_t, resid_t = last_sigma, last_resid
            for day in range(horizon_days):
                sigma_t = np.sqrt(omega + alpha * resid_t**2 + beta * sigma_t**2)
                resid_t = sim_residuals[sim, day, i] * sigma_t
                sim_returns[sim, day, i] = resid_t

    cumulative_returns = np.prod(1 + sim_returns, axis=1) - 1
    return cumulative_returns

def calculate_cvar(returns, alpha=0.05):
    sorted_returns = np.sort(returns)
    var_index = int(alpha * len(sorted_returns))
    return -np.mean(sorted_returns[:var_index])

def portfolio_objective(weights, mean_returns, cov_matrix, selected_assets):
    port_return = np.dot(weights, mean_returns[selected_assets])
    port_vol = np.sqrt(weights @ cov_matrix[np.ix_(selected_assets, selected_assets)] @ weights)
    diversification_penalty = np.std(weights)
    sharpe = (port_return - adjusted_rf) / port_vol
    return -(0.9 * sharpe - 0.1 * diversification_penalty)

def optimize_portfolio(mean_returns, cov_matrix, assets_idx):
    selected_assets = list(assets_idx)
    mean_returns_sel = mean_returns[selected_assets]
    cov_matrix_sel = cov_matrix[np.ix_(selected_assets, selected_assets)]
    n = len(selected_assets)

    def diversification(weights):
        return 1 / (np.linalg.norm(weights - 1.0/n)**2 + 1e-6)

    def portfolio_objective(weights):
        port_return = np.dot(weights, mean_returns_sel)
        port_vol = np.sqrt(weights @ cov_matrix_sel @ weights)
        sharpe = (port_return - adjusted_rf) / port_vol
        return -0.9 * sharpe + 0.1 * diversification(weights)

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = [(min_weight, max_weight)] * n
    initial_weights = np.clip(np.ones(n) / n, min_weight, max_weight)

    result = minimize(
        portfolio_objective,
        initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    if result.success:
        return np.clip(result.x, min_weight, max_weight)
    else:
        return None

def main():
    returns_df, crypto_symbols = load_data()
    print("Data loaded.")

    garch_results = {sym: fit_garch(returns_df[sym]) for sym in crypto_symbols}
    std_resids = pd.DataFrame({sym: garch_results[sym].resid / garch_results[sym].conditional_volatility
                                for sym in crypto_symbols}).dropna()
    corr_matrix = std_resids.corr().values
    df_mle = estimate_df_mle(std_resids.values)
    print(f"Estimated df (MLE): {df_mle:.2f}")

    os.makedirs(result_dir, exist_ok=True)
    csv_data, viz_data = [], []

    with open(result_file, "w") as f:
        f.write("Crypto Portfolio Analysis Results\n" + "=" * 50 + "\n")
        for horizon_name, horizon_days in horizons.items():
            print(f"Processing {horizon_name}...")
            cumulative_returns = simulate_returns(horizon_days, garch_results, corr_matrix, crypto_symbols, df_mle)
            lw = LedoitWolf().fit(cumulative_returns)
            cov_matrix = lw.covariance_
            mean_returns = cumulative_returns.mean(axis=0)

            for num_assets in [2, 3, 4]:
                best_sharpe = -np.inf
                best_portfolio = {}
                for asset_idx in itertools.combinations(range(len(crypto_symbols)), num_assets):
                    weights = optimize_portfolio(mean_returns, cov_matrix, asset_idx)
                    if weights is None:
                        continue
                    port_returns = np.dot(cumulative_returns[:, asset_idx], weights)
                    port_sharpe = (port_returns.mean() - adjusted_rf) / port_returns.std()
                    port_cvar = calculate_cvar(port_returns)
                    asset_list = [crypto_symbols[i] for i in asset_idx]

                    csv_data.append({
                        "num_aset": num_assets,
                        "period": horizon_name,
                        "Asset list": asset_list,
                        "asset bobot": weights.round(4).tolist(),
                        "sharpe ratio": port_sharpe,
                        "cvar": port_cvar
                    })
                    viz_data.append([horizon_name, num_assets, port_sharpe, port_cvar])

                    if port_sharpe > best_sharpe:
                        best_sharpe = port_sharpe
                        best_portfolio = {"assets": asset_list, "weights": weights.round(4).tolist(),
                                          "sharpe_ratio": port_sharpe, "cvar": port_cvar}

                if best_portfolio:
                    f.write(f"\nBest Portfolio for {num_assets} assets ({horizon_name}):\n")
                    f.write(f"Assets: {', '.join(best_portfolio['assets'])}\n")
                    f.write(f"Weights: {best_portfolio['weights']}\n")
                    f.write(f"Sharpe Ratio: {best_portfolio['sharpe_ratio']:.4f}\n")
                    f.write(f"CVaR: {best_portfolio['cvar']:.4f}\n")
                    f.write("-" * 50 + "\n")

    pd.DataFrame(csv_data).to_csv(csv_file, index=False)
    
if __name__ == "__main__":
    main()