#'matplotlibfinances' needs to be installed
#!pip install mplfinance

import pandas as pd
import matplotlib.pyplot as plt #MEGA API for charts and graphs
import matplotlib.dates as mdates
import mplfinance as mpf
import yfinance as yf #yahoo api
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#requesting PETROBRAS' data from Yahoo's API for the entire year of 2023 ...
#... and setting it into the dataframe
dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-23')

#renaming all columns from dataframe
dados.columns = ['Abertura', 'Maximo', 'Minimo', 'Fechamento', 'Fech_Ajust', 'Volume']

#renaming the 'y' axis
dados.rename_axis('Data')

dados['Fechamento'].plot(figsize=(10,6)) #creating a graph based (plot) on column "Fechamento", and setting its dimensions
plt.title('Variacao do preco por data', fontsize=16) #changing title of graph using matplot
plt.legend(['Fechamento']) #adding a legend (legenda) to the graph

df = dados.head(60).copy() #creating a dataframe based on the first 60 instances of dataframe 'dados'
df['Data'] = df.index #converting 'index' to a date-type column

df['Data'] = df['Data'].apply(mdates.date2num) #converting dates to the standard MatPlotLib format, so it can properly create the graphs
#df


# == Generating graphs through MatPlotLib ==

fig, ax = plt.subplots(figsize=(15,8)) #'fig' is the graph, 'ax' will be the axis

width = 0.7 #setting dimensions for the graph's candles

# going through dataframe
for i in range(len(df)):
  # checking if instance is greater than on the beginning of the day for variations
  # ... and setting the colour accordingly
  # PS: 'iloc' is the same as 'indexOf' for both rows and columns
  if df['Fechamento'].iloc[i] > df['Abertura'].iloc[i]:
    color = 'green'
  else:
    color = 'red'

  #setting up the graph's components
  # \-> lines
  ax.plot([df['Data'].iloc[i], df['Data'].iloc[i]],
          [df['Minimo'].iloc[i], df['Maximo'].iloc[i]],
          color=color,
          linewidth=1)

  #setting the dimensions for the graph itself
  # \-> blocks\rectangles
  ax.add_patch(plt.Rectangle((df['Data'].iloc[i] - width/2, min(df['Abertura'].iloc[i], df['Fechamento'].iloc[i])),
                             width,
                             abs(df['Fechamento'].iloc[i] - df['Abertura'].iloc[i]),
                             facecolor=color))

# calculating 'médias móveis' for the following tickers
df['MA7'] = df['Fechamento'].rolling(window=7).mean() #mean() == average
df['MA14'] = df['Fechamento'].rolling(window=14).mean()

# --| Building the graphs(plots) |--
# \-> basis: ax.plot(x, y, color, label)
ax.plot(df['Data'], df['MA7'], color='orange', label='Média Movel 7 dias')
ax.plot(df['Data'], df['MA14'], color='yellow', label='Média Movel 14 dias')

# adding a legend to the graph based on labels
ax.legend()

#formatting dates
ax.xaxis_date() #pointing towards the 'x' axis' date values
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) #setting the standard date format
plt.xticks(rotation=45)

#labeling the axis
plt.title('Gráfico de Candlestick - PETR4.SA com matplotlib') #title for the entire graph
plt.xlabel('Data') #'x' axis
plt.ylabel('Preço') #'y' axis

#enabling a grid display onto the graph
plt.grid(True)

#showing the graph itself
plt.show()

# --| / |--


# == Generating graphs through Plotly.graph_objects ==
# PS: interactive graph

#setting up the graph
# \-> shared_xaxes == sharing the x & y axis with one another
fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=('Candlestick', 'Volume Transicionado'),
                    row_width=[0.2, 0.7])

#adding the candlestick section
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Abertura'],
                             high=df['Maximo'],
                             low=df['Minimo'],
                             close=df['Fechamento'],
                             name='Candlestick'),
                             row=1, col=1)

#adding the 'Médias Móveis' section
#... for the first 7 days ...
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA7'],
                         mode='lines',
                         name='MA7 - Média Móvel 7 dias'),
                         row=1, col=1)

#... and for the first 14 days
fig.add_trace(go.Scatter(x=df.index,
                         y=df['MA14'],
                         mode='lines',
                         name='MA14 - Média Móvel 14 dias'),
                         row=1, col=1)

#adding a 'Volume' section
fig.add_trace(go.Bar(x=df.index,
                     y=df['Volume'],
                     name='Volume'),
                     row=2, col=1)

#changing axis labels
fig.update_layout(yaxis_title='Preço',
                  xaxis_rangeslider_visible=False,
                  width=1100, height=600)

#displaying graph
fig.show()

# == / ==

#re-downloading data, so it's not tampered with
dados = yf.download('PETR4.SA', start='2023-01-01', end='2023-12-23')

# == Generating using MatPlotLib Finances API ==
#creating a candlestick graph(plot) using the first 30 instances, using yahoo's colour palette
mpf.plot(dados.head(30), type='candle', figsize=(16, 8), volume=True, mav=(7, 14), style='yahoo')

# == / ==