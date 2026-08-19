import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


# =========================
# EQUITYLENS
# Indian Equity Analytics Platform
# Developed By Tanay Arora
# =========================

app = Dash(__name__)

app.title = "EquityLens"


# =========================
# Helper Functions
# =========================

def get_stock_data(ticker):
    data = yf.download(
        ticker,
        period="1y",
        interval="1d",
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        return pd.DataFrame()

    # Handle yfinance multi-index columns
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()

    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()

    data["Daily Return"] = data["Close"].pct_change()

    return data


def calculate_metrics(data):

    returns = data["Daily Return"].dropna()

    total_return = (
        data["Close"].iloc[-1] /
        data["Close"].iloc[0] - 1
    ) * 100
    # Trend Signal
    latest_ma20 = data["MA20"].iloc[-1]
    latest_ma50 = data["MA50"].iloc[-1]
    latest_close = data["Close"].iloc[-1]

    if latest_close > latest_ma20 > latest_ma50:
        trend = "Bullish"
    elif latest_close < latest_ma20 < latest_ma50:
        trend = "Bearish"
    else:
        trend = "Neutral"

    if trend == "Bullish":
        signal = "BUY"
        signal_reason = "Price is above both moving averages and MA20 is above MA50."
    elif trend == "Bearish":
        signal = "SELL"
        signal_reason = "Price is below both moving averages and MA20 is below MA50."
    else:
        signal = "HOLD"
        signal_reason = "Price and moving averages do not show a clear bullish or bearish trend."
    volatility = returns.std() * np.sqrt(252) * 100

    cumulative_returns = (1 + returns).cumprod()
    running_max = cumulative_returns.cummax()

    drawdown = (
        cumulative_returns / running_max - 1
    )

    max_drawdown = drawdown.min() * 100

    risk_free_rate = 0.06 / 252

    excess_returns = returns - risk_free_rate

    sharpe_ratio = (
        excess_returns.mean() /
        returns.std()
    ) * np.sqrt(252)

    return {
        "total_return": total_return,
        "volatility": volatility,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe_ratio,
        "trend" : trend,
        "signal": signal,
        "signal_reason": signal_reason,
        "trend_reason": f"Price: ₹{latest_close:.2f} | MA20: ₹{latest_ma20:.2f} | MA50: ₹{latest_ma50:.2f}"
    }


# =========================
# Professional Dashboard Layout
# =========================

app.layout = html.Div(

    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#0b1220",
        "minHeight": "100vh",
        "padding": "30px 50px",
        "color": "#ffffff"
    },

    children=[

# =========================
# Header
# =========================

html.Div(
    [
        html.H1(
            "EquityLens",
            style={
                "textAlign": "center",
                "marginBottom": "5px"
            }
        ),

        html.H3(
            "Indian Equity Analytics Platform",
            style={
                "textAlign": "center",
                "color": "#94a3b8",
                "fontSize": "15px",
                "marginTop": "0px"
            }
        ),

        html.P(
            "Developed by Tanay Arora",
            style={
                "textAlign": "center",
                "color": "#94a3b8",
                "fontSize": "13px",
                "fontStyle": "italic",
                "marginTop": "8px"
            }
        )
    ],

    style={
        "marginBottom": "35px"
    }
),

        # =========================
        # Stock Selector
        # =========================

        html.Div(
            [
                html.Label(
                    "SELECT EQUITY",
                    style={
                        "fontSize": "12px",
                        "fontWeight": "700",
                        "color": "#94a3b8",
                        "letterSpacing": "1px"
                    }
                ),

                dcc.Dropdown(

                    id="stock-selector",

                    options=[
                        {
                            "label": "Reliance Industries",
                            "value": "RELIANCE.NS"
                        },
                        {
                            "label": "Tata Consultancy Services",
                            "value": "TCS.NS"
                        },
                        {
                            "label": "Infosys",
                            "value": "INFY.NS"
                        },
                        {
                            "label": "HDFC Bank",
                            "value": "HDFCBANK.NS"
                        },
                        {
                            "label": "ICICI Bank",
                            "value": "ICICIBANK.NS"
                        },
                        {
                            "label": "State Bank of India",
                            "value": "SBIN.NS"
                        }
                    ],

                    value="RELIANCE.NS",

                    clearable=False,

                    style={
                        "marginTop": "8px",
                        "color": "#111827"
                    }
                )
            ],

            style={
                "backgroundColor": "#111c2e",
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "25px"
            }
        ),

        # =========================
        # Price Chart
        # =========================

        html.Div(

            dcc.Graph(
                id="price-chart",
                config={
                    "displayModeBar": True,
                    "displaylogo": False
                }
            ),

            style={
                "backgroundColor": "#111c2e",
                "borderRadius": "12px",
                "padding": "10px",
                "marginBottom": "30px"
            }
        ),

        # =========================
        # Metrics Header
        # =========================

        html.H2(
            "Risk & Return Metrics",
            style={
                "fontSize": "24px",
                "marginBottom": "18px"
            }
        ),

        # =========================
        # Metric Cards
        # =========================

        html.Div(

            id="metrics",

            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(5, 1fr)",
                "gap": "15px",
                "marginBottom": "30px"
            }
        ),

        # =========================
        # Footer
        # =========================

        html.Div(
            [
                html.Hr(
                    style={
                        "border": "0",
                        "borderTop": "1px solid #243244"
                    }
                ),

                html.P(
                    "EquityLens • Developed by Tanay • Market analytics powered by Python & Yahoo Finance",
                    style={
                        "textAlign": "center",
                        "color": "#64748b",
                        "fontSize": "12px"
                    }
                ),

                html.P(
                    "For educational and informational purposes only. Not financial advice.",
                    style={
                        "textAlign": "center",
                        "color": "#64748b",
                        "fontSize": "11px"
                    }
                )
            ]
        )
    ]
)
# =========================
# Callback
# =========================

@app.callback(

    [
        Output("price-chart", "figure"),
        Output("metrics", "children")
    ],

    Input("stock-selector", "value")
)


def update_dashboard(ticker):

    data = get_stock_data(ticker)

    if data.empty:

        return (
            go.Figure(),
            html.H3("Unable to fetch stock data.")
        )

    metrics = calculate_metrics(data)

    company_name = ticker.replace(".NS", "")

    # =========================
    # Price Chart
    # =========================

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Closing Price"
        )
    )

    fig.add_trace(

        go.Scatter(
            x=data.index,
            y=data["MA20"],
            mode="lines",
            name="20-Day MA"
        )
    )

    fig.add_trace(

        go.Scatter(
            x=data.index,
            y=data["MA50"],
            mode="lines",
            name="50-Day MA"
        )
    )

    fig.update_layout(

        title=f"{company_name} - Price & Moving Averages",

        xaxis_title="Date",

        yaxis_title="Price (₹)",

        template="plotly_dark",
        paper_bgcolor="#111c2e",
        plot_bgcolor="#111c2e",
        font=dict(color="#ffffff"),

        hovermode="x unified"
    )


    # =========================
    # Metric Cards
    # =========================

    cards = [

        html.Div(
            [
                html.H4("Total Return"),
                html.H2(
                    f"{metrics['total_return']:.2f}%"
                )
            ],
            style={
                "padding": "20px",
                "backgroundColor": "#111c2e",
                "color": "#ffffff",
                "borderRadius": "12px",
                "border": "1px solid #243244",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.25)"
            }
        ),

        html.Div(
            [
                html.H4("Annualized Volatility"),
                html.H2(
                    f"{metrics['volatility']:.2f}%"
                )
            ],
            style={
                "padding": "20px",
                "backgroundColor": "#111c2e",
                "color": "#ffffff",
                "borderRadius": "12px",
                "border": "1px solid #243244",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.25)"
            }
        ),

        html.Div(
            [
                html.H4("Maximum Drawdown"),
                html.H2(
                    f"{metrics['max_drawdown']:.2f}%"
                )
            ],
            style={
                "padding": "20px",
                "backgroundColor": "#111c2e",
                "color": "#ffffff",
                "borderRadius": "12px",
                "border": "1px solid #243244",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.25)"
            }
        ),

        html.Div(
            [
                html.H4("Sharpe Ratio"),
                html.H2(
                    f"{metrics['sharpe']:.2f}"
                )
            ],
            style={
                "padding": "20px",
                "backgroundColor": "#111c2e",
                "color": "#ffffff",
                "borderRadius": "12px",
                "border": "1px solid #243244",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.25)"
            }
        ),
        html.Div(
            [
                html.H4(
                    "Trend Signal",
                    style={
                        "color": "#94a3b8",
                        "marginBottom": "10px"
                    }
                ),

                html.H2(
                    f"{metrics['signal']}",
                    style={
                        "fontSize": "30px",
                        "fontWeight": "700",
                        "color": (
                            "#22c55e"
                            if metrics["signal"] == "BUY"
                            else "#ef4444"
                            if metrics["signal"] == "SELL"
                            else "#f59e0b"
                        )
                    }
                ),

                html.P(
                    metrics["signal_reason"],
                    style={
                        "color": "#cbd5e1",
                        "fontSize": "13px",
                        "lineHeight": "1.5"
                    }
                )
            ],

            style={
                "padding": "20px",
                "backgroundColor": "#111c2e",
                "color": "#ffffff",
                "borderRadius": "12px",
                "border": "1px solid #243244",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.25)"
            }
        )
    ]


    return fig, cards


# =========================
# Run Application
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )