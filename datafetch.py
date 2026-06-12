#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# master
"""
Created on Mon Mar  9 11:45:41 2026

@author: mario
"""
## libraries
from datetime import datetime
from scipy.optimize import minimize #solver
import yfinance as yf
import pandas as pd
import numpy as np

## Initial inputs
print("Enter ticker(s)")
end_date = datetime.today()
start_date = end_date.replace(year=end_date.year - 5) # 5yr window
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

while True:
    name = input("Ticker: ")
    ticker = name.strip().upper()
    df = yf.download(
            ticker, #t
            start=start_date, #s
            end=end_date, #e
            auto_adjust=False, 
            progress=False)
    if df.empty or "Adj Close" not in df.columns:
        print("Invalid ticker(s), try again.")
    else:
        prices = df["Adj Close"]
        dr = prices.pct_change().dropna()

        if dr.empty:
            print("Invalid ticker(s), try again.")
        else:
            break

## select rf rate
rf_rate_input = input("\nRisk-free rate, e.g. (0.03): ").strip()

if not rf_rate_input.replace(".", "", 1).isdigit():
    print("Invalid input, defaulting to 0.03.")
    rf_rate = 0.03
else:
    rf_rate = float(rf_rate_input)

## select return frequency
return_frequency = input("\nSelect return frequency, e.g. 'daily'/'monthly':"
                         ).strip().lower()
if return_frequency not in ["daily", "monthly"]:
    print("Invalid input, defaulting to daily returns.")
    return_frequenct = "daily"

# returns calculation
if return_frequency == "daily":
    returns = dr
    periods_per_year = 252
else:
    returns = prices.resample("M").last().pct_change().dropna()
    periods_per_year = 12

mean_returns = returns.mean() * periods_per_year
num_assets = len(mean_returns)

print("\n INDIVIDUAL ASSET (annualized) EXPECTED RETURNS:")
print(mean_returns)

# covariance matrix
matrix = dr.cov() * 252
print("\n ASSET COVARIANCE MATRIX:")
print(matrix)

print("\n NO. OF ASSETS IN PORTFOLIO:")
print(num_assets)

#### Constraints
# 1. Weight sum = 1
# 2. No short selling, i.e. w > 0
# 3. No leveraged assets, i.e. w < 1

## fixed weights
fixed_weights = np.array([1 / num_assets] * num_assets)
fixed_p_return = np.dot(fixed_weights, mean_returns)
fpr_percent = fixed_p_return 
fpr_percent = format(fpr_percent, ".2%")
f_p_sd = np.sqrt(np.dot(fixed_weights.T, np.dot(matrix,fixed_weights)))
f_p_sd_percent = format(f_p_sd, ".2%")
print("\n The expected yearly return of your portfolio is", fpr_percent, "volatility", f_p_sd_percent)

## optimized weights
# sharpe = (p_return - rf_rate) / p_volatility

def p_return(weights):
    return np.dot(weights, mean_returns)

def p_sd(weights):
    return np.sqrt(np.dot(weights.T, np.dot(matrix, weights))) # MMULT

def n_sharpe(weights):
    return -((p_return(weights) - rf_rate) / p_sd(weights))

### constraints 
## no leverage / short selling allowed 
bounds = tuple((0,1) for asset in range(num_assets))

## weight sum = 1
constraints = ({"type": "eq",
                "fun": lambda weights: np.sum(weights) - 1}) 

optimization = minimize(
    n_sharpe,
    fixed_weights,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints)

optimal_weights = optimization.x
optimal_return = p_return(optimal_weights)
optimal_volatility = p_sd(optimal_weights)
optimal_sharpe = (optimal_return - rf_rate) / optimal_volatility

print("\nOPTIMAL ASSET WEIGHTS:")
for ticker, weight in zip(mean_returns.index, optimal_weights):
    print(f"{ticker}: {weight:.2%}")

