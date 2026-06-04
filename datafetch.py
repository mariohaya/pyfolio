#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# master
"""
Created on Mon Mar  9 11:45:41 2026

@author: mario
"""
## libraries
from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np

## Initial inputs
print("Enter ticker(s)")
name = input("Ticker: ")
ticker = name.strip().upper() # tickers
end_date = datetime.today()
start_date = end_date.replace(year=end_date.year - 5) # 5yr window
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

df = yf.download(
    ticker, #t
    start=start_date, #s
    end=end_date, #e
    auto_adjust=False, 
    progress=False
    )

#daily returns
prices = df["Adj Close"]
dr = prices.pct_change().dropna()

# avg annualized returns
mean_returns = dr.mean() * 252
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
# 3. No leveraged assets, i.e. w > 1

## weights
fixed_weights = np.array([1 / num_assets] * num_assets)
fixed_portfolio_return = np.dot(fixed_weights, mean_returns)
print("\n Expected portfolio returns (fixed weights)")
print(fixed_portfolio_return)


