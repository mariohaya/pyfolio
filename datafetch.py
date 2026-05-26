#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 11:45:41 2026

@author: mario
"""
##### libs
from datetime import datetime
import yfinance as yf
import pandas as pd


##### Initial input
print("Enter ticker(s)")
name = input("Ticker: ")

# ticker
ticker = name.strip().upper()

# date range
##start_date = "2025-12-01"
##end_date= "2026-01-10"
end_date = datetime.today()
start_date = end_date.replace(year=end_date.year - 5)
# string format
start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

df = yf.download(
    ticker,
    start=start_date,
    end=end_date,
    auto_adjust=False,
    progress=False
    )

#daily ret
prices = df["Adj Close"]
dr = prices.pct_change().dropna()

print(dr.head())

