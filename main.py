import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from prophet import Prophet #used for time series (finances, etc)

#getting data from Johnson and Johnsons'
dados = yf.download('JNJ', start='2020-01-01', end='2023-12-31', progress=False)
dados = dados.reset_index() #forcing data to be a dataframe, and not a vector

#getting data from columns based on specific dates
dados_treino = dados[dados['Date'] < '2023-07-31']
dados_teste = dados[dados['Date'] >= '2023-07-31']

#renaming columns for the data that'll be used with Prophet
# 'ds' is the value used by Prophet, and 'y' is the data to be estimated by the API, hence the need for renaming
dados_prophet_treino = dados_treino[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})


# ++ Training the Prophet model ++

# determining types of patterns, based on time, to be found on dataframe (daily, weekly & yearly)
modelo = Prophet(weekly_seasonality=True,
                 yearly_seasonality=True,
                 daily_seasonality=False)

# setting if holidays would count towards the training
modelo.add_country_holidays(country_name='US')

# fit() starts the training process
modelo.fit(dados_prophet_treino)

# create future dates for the predictions until 2023
futuro = modelo.make_future_dataframe(periods=150)
previsao = modelo.predict(futuro) #launching prediction
#previsao #printing dataframe for the prediction

# ++ / ++

# setting graph's dimensions
plt.figure(figsize=(14,8))

# creating a plot based on input data
plt.plot(dados_treino['Date'], dados_treino['Close'], label='Dados de Treino', color='blue')

#'' training data (math and statistics)
plt.plot(dados_teste['Date'], dados_teste['Close'], label= 'Dados Reais (teste)', color='green')

#'' prediction data
plt.plot(previsao['ds'], previsao['yhat'], label='Previsão', color='orange', linestyle='--')

# creating a limit based on date
plt.axvline(dados_treino['Date'].max(), color='red', linestyle='--', label='Início da Previsão')

# labeling
plt.xlabel('Data')
plt.ylabel('Preço de Fechamento')
plt.title('Previsão de Preço de Fechamento vs Dados Reais')
plt.legend()

# showing graph
plt.show()
