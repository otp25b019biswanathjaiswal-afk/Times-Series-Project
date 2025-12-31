import plotly.graph_objects as go
import dateutil
import datetime

from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD


# -------------------- TABLE --------------------
def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b></b>"] + ["<b>" + str(i)[:30] + "</b>" for i in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),
            height=35,
        ),
        cells=dict(
            values=[["<b>" + str(i) + "</b>" for i in dataframe.index]] +
                   [dataframe[i] for i in dataframe.columns],
            fill_color=[[rowOddColor, rowEvenColor] * (len(dataframe) // 2 + 1)],
            align='left',
            line_color='white',
            font=dict(color='black', size=15),
        )
    )])

    fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
    return fig


# -------------------- FILTER DATA --------------------
def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1, 1)
    else:
        date = dataframe.index[0]

    df = dataframe.reset_index()
    return df[df['Date'] > date]


# -------------------- CLOSE PRICE CHART --------------------
def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             name='Open', line=dict(width=2, color='#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             name='Close', line=dict(width=2, color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             name='High', line=dict(width=2, color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             name='Low', line=dict(width=2, color='red')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, plot_bgcolor='white', paper_bgcolor='#f1efff')

    return fig


# -------------------- CANDLESTICK --------------------
def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'],
        high=dataframe['High'],
        low=dataframe['Low'],
        close=dataframe['Close']
    ))

    fig.update_layout(height=500, showlegend=False,
                      plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig


# -------------------- RSI --------------------
def RSI(dataframe, num_period):
    rsi = RSIIndicator(close=dataframe['Close'], window=14)
    dataframe['RSI'] = rsi.rsi()

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['RSI'],
                             name='RSI', line=dict(width=2, color='orange')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[70]*len(dataframe),
                             name='Overbought', line=dict(dash='dash', color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=[30]*len(dataframe),
                             name='Oversold', line=dict(dash='dash', color='green')))

    fig.update_layout(height=200, yaxis_range=[0, 100],
                      plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig


# -------------------- MOVING AVERAGE --------------------
def Moving_average(dataframe, num_period):
    sma = SMAIndicator(close=dataframe['Close'], window=50)
    dataframe['SMA_50'] = sma.sma_indicator()

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             name='Close', line=dict(color='black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                             name='SMA 50', line=dict(color='purple')))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig


# -------------------- MACD --------------------
def MACD_plot(dataframe, num_period):
    macd = MACD(close=dataframe['Close'])

    dataframe['MACD'] = macd.macd()
    dataframe['MACD Signal'] = macd.macd_signal()
    dataframe['MACD Hist'] = macd.macd_diff()

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD'],
                             name='MACD', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['MACD Signal'],
                             name='Signal', line=dict(color='red')))

    fig.update_layout(height=250, plot_bgcolor='white', paper_bgcolor='#e1efff')
    return fig


# -------------------- FORECAST CHART --------------------
def Moving_average_forecast(forecast):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=forecast.index[:-30],
        y=forecast['Close'].iloc[:-30],
        name='Close Price',
        line=dict(color='black')
    ))

    fig.add_trace(go.Scatter(
        x=forecast.index[-30:],
        y=forecast['Close'].iloc[-30:],
        name='Future Price',
        line=dict(color='red')
    ))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, plot_bgcolor='white', paper_bgcolor='#e1efff')

    return fig
