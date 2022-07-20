import pandas as pd
from sympy import comp
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
## 表示日数を指定
""")

days = st.sidebar.slider("表示日数を指定してください。",1,360,30)

st.write(f"""
### 過去**{days}日間**の株価を表示
""")

st.sidebar.write("""
## 株価の範囲指定
""")
ymin, ymax = st.sidebar.slider(
    "範囲を指定してください。",
    0.0,3500.0,(0.0,5000.0)
)

#銘柄を指定
tickers = {
    "第一生命" : "8750.T",
    "かんぽ生命":"7181.T",
    "MS&AD":"8725.T",
    "ライフネット生命":"7157.T",
    "SBIインシュランス":"7236.T",
}

def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df


df = get_data(days, tickers)


companies = st.multiselect(
    "会社名を選択してください。",
    list(df.index),
    ['第一生命', 'かんぽ生命', 'MS&AD']
)


data = df.loc[companies]
st.write(data.sort_index())
data = data.T.reset_index()
data = pd.melt(data, id_vars=['Date']).rename(columns={"value": "Stockprice"})
chart = (
    alt.Chart(data)
    .mark_line(opacity=0.7, clip=True)
    .encode(
        x="Date:T",
        y=alt.Y("Stockprice:Q", stack=None, scale=alt.Scale(domain=[ymin,ymax])),
        color="Name:N"
    )
)
st.altair_chart(chart, use_container_width=True)