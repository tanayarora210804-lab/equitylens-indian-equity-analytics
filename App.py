import yfinance as yf
import plotly.graph_objects as go

print("===================================")
print("          EQUITYLENS")
print("   Indian Equity Analytics Platform")
print("===================================")

# -----------------------------------
# 1. Download stock data
# -----------------------------------

ticker = "RELIANCE.NS"

data = yf.Ticker(ticker).history(period="1y")

# -----------------------------------
# 2. Calculate moving averages
# -----------------------------------

data["MA20"] = data["Close"].rolling(window=20).mean()
data["MA50"] = data["Close"].rolling(window=50).mean()

# -----------------------------------
# 3. Create chart
# -----------------------------------

fig = go.Figure()

# Closing price
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Closing Price"
    )
)

# 20-day moving average
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["MA20"],
        mode="lines",
        name="20-Day MA"
    )
)

# 50-day moving average
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["MA50"],
        mode="lines",
        name="50-Day MA"
    )
)

# -----------------------------------
# 4. Chart layout
# -----------------------------------

fig.update_layout(
    title="Reliance Industries - Price & Moving Averages",
    xaxis_title="Date",
    yaxis_title="Price (₹)",
    template="plotly_white",
    hovermode="x unified"
)

# -----------------------------------
# 5. Display chart
# -----------------------------------

fig.show()
data["MA50"] = data["Close"].rolling(window=50).mean()
# -----------------------------------
# 3. Returns & Risk Analysis
# -----------------------------------

# Daily returns
data["Daily Return"] = data["Close"].pct_change()

# Total return over the period
total_return = (
    (data["Close"].iloc[-1] / data["Close"].iloc[0]) - 1
) * 100

# Annualized volatility
volatility = data["Daily Return"].std() * (252 ** 0.5) * 100

# Maximum drawdown
rolling_max = data["Close"].cummax()
drawdown = (data["Close"] - rolling_max) / rolling_max
max_drawdown = drawdown.min() * 100

# Sharpe ratio
risk_free_rate = 0.06

annual_return = data["Daily Return"].mean() * 252
annual_volatility = data["Daily Return"].std() * (252 ** 0.5)

sharpe_ratio = (
    (annual_return - risk_free_rate) / annual_volatility
)

# Print metrics
print("\n========== RISK & RETURN ==========")
print(f"Total Return: {total_return:.2f}%")
print(f"Annualized Volatility: {volatility:.2f}%")
print(f"Maximum Drawdown: {max_drawdown:.2f}%")
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")