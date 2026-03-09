#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 11:45:41 2026

@author: mario
"""
##### libs
import yfinance as yf
import pandas as pd

##### Initial input
print("Enter ticker(s)")
name = input("Ticker: ")

# ticker, date range (yyyy-mm-dd)
ticker = name.strip().upper()
start_date = "2025-12-01"
end_date= "2026-01-10"

df = yf.download(
    ticker,
    start=start_date,
    end=end_date,
    auto_adjust=False,
    progress=False
    )

print(df.head())


