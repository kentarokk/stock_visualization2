import pandas as pd
import yfinance as yf
from datetime import datetime as dt
import altair as alt
import streamlit as st


st.title("生命保険会社の株価を可視化")

st.sidebar.write("""
# 使い方
こちらは株価可視化ツールです。以下のオプションを指定してください。
""")

st.sidebar.write("""
# 表示日数を選択してください。
""")

days = st.sidebar.slider("表示日数",1,60,30)