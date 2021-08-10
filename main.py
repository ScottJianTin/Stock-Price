import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date

st.write("""
# Financial Dashboard
""")

## define the ticker symbol (e.g. AAPL - Apple, AMZN - Amazon, MSFT - Microsoft)
tickerSymbol = st.selectbox("Select Stock", ("Facebook (FB)", "Apple (AAPL)", "Amazon (AMZN)", "Netflix (NFLX)", "Google (GOOGL)", "Other"))
if tickerSymbol == "Other":
    tickerSymbol = st.text_input("Ticker Symbol (e.g. MSFT)")
    tickerData = yf.Ticker(tickerSymbol)
else:
    tickerData = yf.Ticker(tickerSymbol[tickerSymbol.find("(") + 1:tickerSymbol.find(")")]) # get data on this sticker

# tickerData.info  ### uncomment to see more info about the yf ticker data

## get the historical prices for this ticker
start_date = st.date_input("Start Date", date(2010,6,30))
end_date = st.date_input("End Date", date(2020,6,30))
tickerDf = tickerData.history(period="1d", start=start_date, end=end_date)
## Open, High, Low, Close, Volume, Dividends, Stock, Splits

## search button
search_button = st.button("Search")

## show statistics based on user input when search button is pressed
if search_button:
    st.write(f"""
    ***
    # Stock overview: {tickerSymbol}
    """)

    ## Ticker Info
    info = tickerData.info

    st.subheader("Business Summary")
    summary = info["longBusinessSummary"].split(".")[:5]
    st.write(".".join(summary))

    st.subheader("Location")
    st.write(f"""
    {info["city"]}, {info["state"]}, {info["country"]}
    """)

    st.subheader("Statistics")
    stat_df = pd.DataFrame({"Profit Margins": info["profitMargins"],
                            "Revenue Growth": info["revenueGrowth"],
                            "EBITDA": info["ebitda"],
                            "Market Cap": info["marketCap"],
                            "Buy(1) / Sell(0)": 1 if info["recommendationKey"]=="buy" else 0,
                            "Current Price": info["currentPrice"],
                            "Dividend Rate": info["dividendRate"],
                            "Payout Ratio": info["payoutRatio"],
                            "Earnings Growth": info["earningsGrowth"],
                            "Gross Profit": info["grossProfits"],
                            "Free Cash Flow": info["freeCashflow"],
                            "Current Ratio": info["currentRatio"],
                            "Quick Ratio": info["quickRatio"],
                            "Debt To Equity": info["debtToEquity"],
                            "Return on Equity": info["returnOnEquity"]},
                            index=["values"])
    stat_df = pd.melt(stat_df)
    st.write(stat_df)

    st.subheader("Financials")
    tickerData.financials

    st.subheader("Actions (Dividends, Splits)")
    tickerData.actions

    st.subheader("Major Holders")
    tickerData.major_holders

    st.subheader("Institutional Holders")
    tickerData.institutional_holders

    # st.subheader("Corporate Sustainability")
    # tickerData.sustainability

    st.subheader("Balance Sheet")
    tickerData.balancesheet

    st.subheader("Cash Flow")
    tickerData.cashflow

    st.subheader("Earnings")
    tickerData.earnings

    st.subheader("Analysts Recommendations")
    tickerData.recommendations

    st.write("***")

    ## Line Chart
    st.write("# Price")

    st.subheader("Closing Price")
    st.line_chart(tickerDf.Close)

    st.subheader("Volume Price")
    st.line_chart(tickerDf.Volume)


## tickerDf.Open, tickerDf.High, tickerDf.Low
